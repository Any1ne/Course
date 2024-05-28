from manim import *
# from manim.camera.camera import Camera
from sympy import *
import json
import math

config.disable_caching = False

class Newtons(ZoomedScene):
    def __init__(self, **kwargs):
        ZoomedScene.__init__(
            self,
            zoom_factor=0.6,
            zoomed_display_height=5,
            zoomed_display_width=7,
            image_frame_stroke_width=20,
            zoomed_camera_config={ "default_frame_stroke_width": 3},
            zoomed_display_corner= [-1., 0., 0.],
            zoomed_camera_frame_starting_position= [0., -6., 0.],
            zoom_activated=True,
            **kwargs
        )

    def construct(self):
        self.activate_zooming()
        # self.zoomed_camera.frame.set_opacity(opacity=0)
        # self.zoomed_display.display_frame.set_opacity(opacity=1) 
        print("init")
        self.init()
        self.title = Title("Newton's Method")
        self.add(self.title)

        if self.iter ==1:
            print("axes")
            self.axes()
            print("function")
            self.function()
            print("create_X")
            self.create_X()
        # else:
        #     print("continue_prev")
        #     self.continue_prev()
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

        self.x0 = config['x0']
        self.xi = config['xi']
        self.xi_1 = config['xi+1']
        self.iter = config['Iteration']
        self.rest = config['Rest']
        self.fxi = config['f(xi)']
        self.fx0 = config['f(x0)']
        self.fxi_1 = config['f(xi+1)']

        x = symbols('x')
        self.func_expr = sympify(config['f(x)'])
        self.tang_expr = sympify(config['tangent'])
        self.X = ValueTracker(self.xi)
        
        self.xmin = ValueTracker(self.rest[0])
        self.xmax = ValueTracker(self.rest[1])
        self.xstep = 1

        # self.ystep = ValueTracker(1)
        # self.scale_level=0

        # yrange = self.calc_zoom(self.fxi)
        # self.ymin = ValueTracker(yrange[0])
        # self.ymax = ValueTracker(yrange[1])

        # self.calculacte_scale(self.ymin.get_value(), self.ymax.get_value())

    def axes(self):
        self.ystep = ValueTracker(1)
        self.scale_level=0

        yrange = self.calc_zoom(self.fx0)
        self.ymin = ValueTracker(yrange[0])
        self.ymax = ValueTracker(yrange[1])

        self.calculacte_scale(self.ymin.get_value(), self.ymax.get_value())
    
        self.ax = self.create_axes(self.ymin.get_value(), self.ymax.get_value(), self.ystep.get_value()).scale(0.5).to_edge(RIGHT, buff=0.5).shift(UP*1)
        self.z_ax = self.create_axes(self.ymin.get_value(), self.ymax.get_value(), self.ystep.get_value()).scale(0.5).to_edge(LEFT, buff=0.5)
        self.add(self.z_ax) 
        self.zoomed_camera.frame.move_to(self.ax)
        self.play(Create(self.ax), run_time = 3)
        
    def create_axes(self, y_min, y_max, y_step):
        ax = Axes(x_range=[self.xmin.get_value(), self.xmax.get_value(), self.xstep],
                  y_range=[y_min, y_max, y_step],
                  x_length=10, y_length=6,
                #   y_axis_config={"numbers_to_include": np.arange(y_min+0.1*y_step, y_max-0.1*y_step, y_step)}
                  )
        return ax
        
    # def update_axes(self, ax, ):
    #     # Re-create the axes with updated ranges
    #     self.calculacte_scale(self.ymin.get_value(), self.ymax.get_value())

    #     new_ax = self.create_axes(self.ymin.get_value(), self.ymax.get_value(), self.ystep.get_value())
    #     self.func = new_ax.plot(lambda x: self.func_expr.subs('x', x), x_range=[self.xmin.get_value(), self.xmax.get_value()], use_smoothing=True, color=RED)
    #     new_ax.add(self.func)    
    #     # Create self.a new graph for the updated axes
        
    #     ax.become(new_ax)

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
        self.clip(self.func, self.ax)
        self.ax.add(self.func)

        self.z_func = self.z_ax.plot(lambda x: self.func_expr.subs('x', x), x_range=[self.xmin.get_value(), self.xmax.get_value()], color=BLUE)

        self.play(Create(VGroup(self.func, self.z_func)), run_time = 1)

    def create_X(self):
        self.x_var = Variable(self.X.get_value(), 'x', num_decimal_places=3).next_to(self.ax, DOWN, buff=0.5)
        self.fx_var = Variable(self.func_expr.subs('x', self.X.get_value()).evalf(), 'f(x)', num_decimal_places=3).next_to(self.x_var, DOWN, buff=0.5)
        self.add(self.x_var, self.fx_var)

        self.xi_label = self.ax.get_T_label(
            x_val=self.xi,
            graph=self.func, 
            label=Tex(f"x{self.iter}")
        )
        self.fxi_label = self.ax.get_graph_label(
            graph=self.func,
            label = "",
            x_val=self.xi,
            dot=True,
            direction=UL,
        )

        self.z_xi_label = self.z_ax.get_T_label(
            x_val=self.xi,
            graph=self.z_func, 
            label=Tex(f"x{self.iter}")
        )
        self.z_fxi_label = self.z_ax.get_graph_label(
            graph=self.z_func,
            label = "",
            x_val=self.xi,
            dot=True,
            direction=UL,
        )
        
        self.play(Create(VGroup(self.xi_label, self.z_xi_label, self.fxi_label, self.z_fxi_label,)), run_time = 3)

    def continue_prev(self):
        #Continue from prev Zoom

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

        x_var = Variable(self.X.get_value(), 'x', num_decimal_places=3).next_to(self.ax, DOWN, buff=0.5)
        fx_var = Variable(self.func_expr.subs('x', self.X.get_value()).evalf(), 'f(x)', num_decimal_places=3).next_to(x_var, DOWN, buff=0.5)
        self.add(x_var, fx_var)

        self.add(VGroup(self.ax, self.func, self.xi_label, self.fxi_label))

    def create_tangent(self):
        self.tangent = self.ax.plot(lambda x:  self.tang_expr.subs('x', x), x_range=[self.xmin.get_value(), self.xmax.get_value()])
        self.z_tangent = self.z_ax.plot(lambda x:  self.tang_expr.subs('x', x), x_range=[self.xmin.get_value(), self.xmax.get_value()])
         
        self.dot_i = self.ax.get_graph_label(
            graph=self.tangent,
            label = "",
            x_val=self.X.get_value(),
            dot=True,
            direction=UR,
            )
        
        self.z_dot_i = self.z_ax.get_graph_label(
            graph=self.z_tangent,
            label = "",
            x_val=self.X.get_value(),
            dot=True,
            direction=UR,
            )
        
        # self.clip(self.tangent, self.ax)
        self.play(Create(VGroup(self.tangent, self.z_tangent, self.dot_i, self.z_dot_i,)), run_time = 3)

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

        self.X.set_value(self.xi_1)
        self.play(self.x_var.tracker.animate.set_value(self.xi_1), self.fx_var.tracker.animate.set_value(self.fxi_1), run_time=1,)

        self.xi_1_label = self.ax.get_T_label(
            label= Tex(f"x{self.iter+1}"),
            x_val=self.X.get_value(),
            graph=self.func, 
        )
        
        self.fxi_1_label = self.ax.get_graph_label(
            graph=self.func,
            label = "",
            x_val=self.X.get_value(),
            dot=True
        )

        self.z_xi_1_label = self.z_ax.get_T_label(
            label= Tex(f"x{self.iter+1}"),
            x_val=self.X.get_value(),
            graph=self.z_func,
            # triangle_size=0.05
        )

        self.z_fxi_1_label = self.z_ax.get_graph_label(
            graph=self.z_func,
            label = "",
            x_val=self.X.get_value(),
            dot=True
        )

        self.play(Create(VGroup(self.xi_1_label, self.z_xi_1_label, self.fxi_1_label, self.z_fxi_1_label)), run_time = 3)

    def delete_old(self):
        self.play(Uncreate(VGroup(self.xi_label, self.z_xi_label, self.fxi_label, self.dot_i, self.z_fxi_label, self.tangent, self.z_tangent, self.dot_i_1)), run_time = 3)

    def zoom_in(self):
        self.zoomed_camera.frame.move_to(self.z_fxi_1_label)
        # self.scale_zoom()
        scale=self.fxi_1/self.fx0
        self.play(self.zoomed_camera.frame.animate.scale(scale))

    def scale_zoom(self):
        x_scale =self.z_xi_1_label.width/self.zoomed_camera.frame.width
        self.z_xi_1_label.set_stroke(width=x_scale)

        # fx_scale =self.z_fxi_1_label/self.zoomed_camera.frame.width
        self.z_fxi_1_label.scale(x_scale)
        func_scale =self.z_func.width/self.zoomed_camera.frame.width
        self.z_func.set_stroke(width=func_scale)
        
    # def fix_dots_sizes(self):
    #     dots = [d for d in self.mobjects if isinstance(d, Dot)]
    #     dot_scale = dots[0].width / self.camera.frame.width

    #     def updater(dot, dt):
    #         dot.set_width(dot_scale * self.camera.frame.width)
    #     for dot in dots:
    #         dot.add_updater(updater)
    
    # def fix_numberplane_linewidth(self):
    #     numberplanes = [d for d in self.mobjects if isinstance(d, NumberPlane)]
    #     line_scale = numberplanes[0].x_axis.stroke_width / self.camera.frame.width

    #     def updater(np, dt):
    #         for l in list(np.background_lines) + [np.get_x_axis(), np.get_y_axis()]:
    #             l.set_stroke(width=line_scale * self.camera.frame.width)
    #     for np in numberplanes:
    #         np.add_updater(updater)

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
