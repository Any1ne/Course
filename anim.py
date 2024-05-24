from manim import *
# from manim.camera.camera import Camera
from sympy import *
import json
import math

class Newtons(Scene):
    def construct(self):
        self.init()

        if self.iter ==1:
          self.axes()
          self.function()
          self.create_X()
        else:
          self.continue_prev()
        # self.tangent()
        # self.update_x()
        # self.delete_old()
        # self.zoom_in()

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

        yrange = self.calc_zoom(self.fxi)
        self.ymin = ValueTracker(yrange[0])
        self.ymax = ValueTracker(yrange[1])
        self.ystep = ValueTracker(yrange[2])

    def axes(self):
        self.ax = self.create_axes(self.ymin.get_value(), self.ymax.get_value(), self.ystep.get_value())
        self.play(Create(self.ax), run_time = 1)
        pass

    def update_axes(self, ax):
        # Re-create the axes with updated ranges
        new_ax = self.create_axes(self.ymin.get_value(), self.ymax.get_value(), self.ystep.get_value())
            
        # Create self.a new graph for the updated axes
        self.func = new_ax.plot(lambda x: self.func_expr.subs('x', x), x_range=[self.xmin.get_value(), self.xmax.get_value()], use_smoothing=True, color=RED)
        new_ax.add(self.func)
        
        ax.become(new_ax)

    def create_axes(self, y_min, y_max, y_step):
        self.ax = Axes(x_range=[self.xmin.get_value(), self.xmax.get_value(), self.xstep],
                  y_range=[y_min, y_max, y_step],
                  y_axis_config={"include_numbers": True}).shift(LEFT)
        return self.ax

    def function(self):
        self.func =  self.ax.plot(lambda x: self.func_expr.subs('x', x), x_range=[self.xmin.get_value(), self.xmax.get_value()], color=BLUE)
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
            label= Tex(f"f(x{self.iter})"),
            x_val=self.xi,
            dot=True,
            direction=UR,
        )

        x_var = Variable(self.xi, 'x', num_decimal_places=3)
        fx_var = Variable(self.func_expr.subs('x', self.xi).evalf(), 'f(x)', num_decimal_places=3)
        vg = Group(x_var, fx_var).arrange(DOWN)

        vg.next_to(self.ax, RIGHT, buff=0.5)
        self.add(x_var, fx_var)
        self.play(x_var.tracker.animate.set_value(0), run_time=2,)

        self.play(Create(VGroup(self.xi_label, self.fxi_label)), run_time = 1)

    def continue_prev(self):
        self.ax = self.create_axes(self.ymin.get_value(), self.ymax.get_value(), self.ystep.get_value())
        self.func =  self.ax.plot(lambda x: self.func_expr.subs('x', x), x_range=[self.xmin.get_value(), self.xmax.get_value()], color=BLUE)
        self.ax.add(self.func)
        self.xi_label = self.ax.get_T_label(
            x_val=self.xi,
            graph=self.func, 
            label=Tex(f"x{self.iter}")
        )
        self.fxi_label = self.ax.get_graph_label(
            graph=self.func,
            label= Tex(f"f(x{self.iter})"),
            x_val=self.xi,
            dot=True,
            direction=UR,
        )
        self.add(VGroup(self.ax, self.func, self.xi_label, self.fxi_label))

    def tangent(self):
        self.tangent = self.ax.plot(lambda x:  self.tang_expr.subs('x', x), x_range=[-5, 5])
         
        self.dot_i = always_redraw(lambda: self.ax.get_graph_label(
            graph=self.tangent,
            label = "",
            x_val=self.X.get_value(),
            dot=True,
            direction=UR,
            )
        )
        self.play(Create(VGroup(self.tangent, self.dot_i)), run_time = 1)

    def update_x(self):
        self.play(self.X.animate.set_value(self.xi_1), run_time = 1)
        
        self.xi_1_label = always_redraw(lambda:self.ax.get_T_label(
            label= Tex(f"x{self.iter+1}"),
            x_val=self.X.get_value(),
            graph=self.func, 
        ))
        
        self.fxi_1_label = always_redraw(lambda:self.ax.get_graph_label(
            graph=self.func,
            label= Tex(f"f(x{self.iter+1})"),
            x_val=self.X.get_value(),
            dot=True,
            direction=UR,
            ))
        
        g = always_redraw(lambda: VGroup(self.ax,self.func, self.xi_1_label,  self.fxi_1_label))
        # func.add(xi_1_label)
        # func.add(fxi_1_label)

        #6)Create label
        self.play(Create(VGroup(self.xi_1_label, self.fxi_1_label)), run_time = 1)

    def delete_old(self):
        self.play(Uncreate(VGroup(self.xi_label, self.fxi_label, self.tangent)), run_time = 1)

    def zoom_in(self):
        yrange = self.calc_zoom(self.fxi_1)

        ##Transform scale 
        self.ax.add_updater(self.update_axes)
        self.ystep.set_value(yrange[2])
        self.play(self.ymax.animate.set_value(yrange[1]), self.ymin.animate.set_value(yrange[0]), run_time = 5)
        self.wait()
        self.ax.remove_updater(self.update_axes)
        self.wait()
        
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
            
            scale = 10 ** (math.floor(math.log10((B-A)/10)))*5
            yrange=[round(A, 5), round(B, 5), round(scale, 6)]
            print(yrange)
            print((B-A)/scale)
            return yrange
