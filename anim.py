from manim import *
# from manim.camera.camera import Camera
from sympy import *
import json
import math

config.disable_caching = False

class Newtons(MovingCameraScene):
    def construct(self):
        print("init")
        self.init()

        self.add(Title("Newton's Method"))
        if self.iter ==1:
            print("axes")
            self.axes()
            print("function")
            self.function()
            print("create_X")
            self.create_X()
        else:
            print("continue_prev")
            self.continue_prev()
        print("tangent")
        self.create_tangent()
        print("update_x")
        self.update_x()
        print("delete_old")
        self.delete_old()
        print("zoom_i")
        self.zoom_in()

    def init(self):
        with open('config.json') as f:
            config = json.load(f)

        self.xi = config['xi']
        self.xi_1 = config['xi+1']
        self.iter = config['Iteration']
        self.rest = config['Rest']
        self.fxi = config['f(xi)']
        self.fxi_1 = config['f(xi+1)']

        x = symbols('x')
        self.func_expr = sympify(config['f(x)'])
        self.tang_expr = sympify(config['tangent'])
        self.X = ValueTracker(self.xi)
        
        self.xmin = ValueTracker(self.rest[0])
        self.xmax = ValueTracker(self.rest[1])
        self.xstep = 1

        self.ystep = ValueTracker(1)
        self.scale_level=0

        yrange = self.calc_zoom(self.fxi)
        self.ymin = ValueTracker(yrange[0])
        self.ymax = ValueTracker(yrange[1])

        self.calculacte_scale(self.ymin.get_value(), self.ymax.get_value())

    def axes(self):
        self.ax = self.create_axes(self.ymin.get_value(), self.ymax.get_value(), self.ystep.get_value())
        self.play(Create(self.ax), run_time = 3)
        
    def create_axes(self, y_min, y_max, y_step):
        self.ax = Axes(x_range=[self.xmin.get_value(), self.xmax.get_value(), self.xstep],
                  y_range=[y_min, y_max, y_step],
                  x_length=10, y_length=6,
                #   y_axis_config={"numbers_to_include": np.arange(y_min+0.1*y_step, y_max-0.1*y_step, y_step)}
                  ).to_edge(DL, buff=0.5)
        return self.ax
        
    def update_axes(self, ax, ):
        # Re-create the axes with updated ranges
        self.calculacte_scale(self.ymin.get_value(), self.ymax.get_value())

        new_ax = self.create_axes(self.ymin.get_value(), self.ymax.get_value(), self.ystep.get_value())
        self.func = new_ax.plot(lambda x: self.func_expr.subs('x', x), x_range=[self.xmin.get_value(), self.xmax.get_value()], use_smoothing=True, color=RED)
        new_ax.add(self.func)    
        # Create self.a new graph for the updated axes
        
        ax.become(new_ax)

    def clip(self, curve, axes):
        points = curve.points
        x_min, x_max = axes.x_range[:2]
        y_min, y_max = axes.y_range[:2]
        for i in range(0,len(points), 4):
            p_start, c_1, c2, p_end = points[i:i+4]
            p1 = axes.p2c(p_start)
            p2 = axes.p2c(p_end)
            if any(p[0] < x_min or p[0] > x_max or p[1] < y_min or p[1] > y_max for p in [p1, p2]):
                points[i:i+4] = [np.array([0,0,0])]*4

    def function(self):
        self.func = self.ax.plot(lambda x: self.func_expr.subs('x', x), x_range=[self.xmin.get_value(), self.xmax.get_value()], color=BLUE)
        # self.clip(self.func, self.ax)
        self.ax.add(self.func)
        self.play(Create(self.func), run_time = 1)

    def create_X(self):
        self.xi_label = self.ax.get_T_label(
            x_val=self.xi,
            graph=self.func, 
            label=Tex(f"x{self.iter}")
        )
        self.fxi_label = self.ax.get_graph_label(
            graph=self.func,
            x_val=self.xi,
            dot=True,
            direction=UL,
        )

        x_var = always_redraw(lambda: Variable(self.X.get_value(), 'x', num_decimal_places=3).next_to(self.ax, RIGHT, buff=1))
        fx_var = always_redraw(lambda: Variable(self.func_expr.subs('x', self.X.get_value()).evalf(), 'f(x)', num_decimal_places=3).next_to(x_var, DOWN, buff=0.5))
        self.add(x_var, fx_var)
        
        self.play(Create(VGroup(self.xi_label, self.fxi_label)), run_time = 3)

    def continue_prev(self):
        self.ax = self.create_axes(self.ymin.get_value(), self.ymax.get_value(), self.ystep.get_value())
        self.func =  self.ax.plot(lambda x: self.func_expr.subs('x', x), x_range=[self.xmin.get_value(), self.xmax.get_value()], color=BLUE)
        # self.clip(self.func, self.ax)
        self.ax.add(self.func)
        self.xi_label = self.ax.get_T_label(
            x_val=self.xi,
            graph=self.func, 
            label=Tex(f"x{self.iter}")
        )
        self.fxi_label = self.ax.get_graph_label(
            graph=self.func,
            x_val=self.xi,
            dot=True
        )

        x_var = always_redraw(lambda: Variable(self.X.get_value(), 'x', num_decimal_places=3).to_edge(RIGHT, buff=0.5))
        fx_var = always_redraw(lambda: Variable(self.func_expr.subs('x', self.X.get_value()).evalf(), 'f(x)', num_decimal_places=3).next_to(x_var, DOWN, buff=0.5))
        self.add(x_var, fx_var)

        self.add(VGroup(self.ax, self.func, self.xi_label, self.fxi_label))

    def create_tangent(self):
        self.tangent = self.ax.plot(lambda x:  self.tang_expr.subs('x', x), x_range=[self.xmin.get_value(), self.xmax.get_value()])
         
        self.dot_i = self.ax.get_graph_label(
            graph=self.tangent,
            label = "",
            x_val=self.X.get_value(),
            dot=True,
            direction=UR,
            )
        # self.clip(self.tangent, self.ax)
        self.play(Create(VGroup(self.tangent, self.dot_i)), run_time = 3)

    def update_x(self):
        self.X.set_value(self.xi_1)

        self.dot_i_1 = self.ax.get_graph_label(
            graph=self.tangent,
            label = "",
            x_val=self.X.get_value(),
            dot=True,
            direction=UR,
        )

        self.play(ReplacementTransform(self.dot_i,self.dot_i_1))

        # self.vg.add_updater(self.update_text)
        self.play(self.X.animate.set_value(self.xi_1), run_time = 1)
        self.wait()
        # self.vg.remove_updater(self.update_text)


        self.xi_1_label = always_redraw(lambda: self.ax.get_T_label(
            label= Tex(f"x{self.iter+1}"),
            x_val=self.X.get_value(),
            graph=self.func, 
        )) 
        
        self.fxi_1_label = always_redraw(lambda: self.ax.get_graph_label(
            graph=self.func,
            x_val=self.X.get_value(),
            dot=True
        ))
        self.play(Create(VGroup(self.xi_1_label, self.fxi_1_label)), run_time = 3)

    def delete_old(self):
        self.play(Uncreate(VGroup(self.xi_label, self.fxi_label, self.tangent)), run_time = 3)

    def zoom_in(self):
        self.camera.frame.save_state()

        self.play(self.camera.frame.animate.scale(0.5).move_to(self.dot_i_1))

        # yrange = self.calc_zoom(self.fxi_1)

        # ##Transform scale 
        # self.ax.add_updater(self.update_axes)
        # #self.ystep.set_value(yrange[2])
        # self.play(self.ymax.animate.set_value(yrange[1]), self.ymin.animate.set_value(yrange[0]), run_time = 3)
        # self.wait()
        # self.ax.remove_updater(self.update_axes)
        # self.wait()
        
    def calc_zoom(self, y, k=1, l=4, m=5):
            d = y/k
            A = (k+l)*d
            B = -m*d

            if A>B:
                temp = A
                A=B
                B=temp
            elif A==B:
                A = y-0.1
                B = y+0.1
            print("ZOOM", A,B)
            
            # scale = 10 ** (math.floor(math.log10((B-A)/10)))*5
            #self.calculacte_scale(A, B)
            yrange=[round(A, 5), round(B, 5)]
            print(yrange)
            print((B-A)/self.ystep.get_value())
            return yrange
    
    def calculacte_scale(self, A, B):
        scale = self.ystep.get_value()

        print(f"Restriction: [{A}, {B}]")
       
        flag = False
        while not flag:
            n_ticks = (B-A)//scale
            print(f"Number of ticks: {n_ticks}")
            print(f"Curent level of scale: {self.scale_level}\n")

            if n_ticks<5:
                # scale down
                if self.scale_level % 3 == 2 :
                    scale*=0.4
                else:
                    scale *= 0.5
                    
                self.scale_level -=1
            elif n_ticks>12:
                # scale up
                if self.scale_level % 3 == 1 :
                    scale /=0.4
                else:
                    scale /= 0.5
                self.scale_level +=1
            else:
                flag = True

        scale = round(scale, 5)
        self.ystep.set_value(scale)