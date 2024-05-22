from manim import *
# from manim.camera.camera import Camera
from sympy import *
import json
import math

class Newtons(Scene):
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
    
    def update_axes(self, ax):
        # Re-create the axes with updated ranges
        new_ax = self.create_axes(self.ymin.get_value(), self.ymax.get_value(), self.ystep.get_value())
            
        # Create self.a new graph for the updated axes
        self.func = new_ax.plot(lambda x: self.func_expr.subs('x', x), x_range=[self.xmin.get_value(), self.xmax.get_value()], use_smoothing=True, color=RED)
        new_ax.add(self.func)
        
        ax.become(new_ax)

    def create_axes(self, y_min, y_max, y_step):
        ax = Axes(x_range=[self.xmin.get_value(), self.xmax.get_value(), self.xstep],
                  y_range=[y_min, y_max, y_step],
                  y_axis_config={"include_numbers": True})
        return ax

    def construct(self):
        self.init()
        ax = self.create_axes(self.ymin.get_value(), self.ymax.get_value(), self.ystep.get_value())
        self.func =  ax.plot(lambda x: self.func_expr.subs('x', x), x_range=[self.xmin.get_value(), self.xmax.get_value()], color=BLUE)
        ax.add(self.func)
        tangent = ax.plot(lambda x:  self.tang_expr.subs('x', x), x_range=[-5, 5])
        
        xi_label = ax.get_T_label(
            x_val=self.xi,
            graph=self.func, 
            label=Tex(f"x{self.iter}")
        )
        fxi_label = ax.get_graph_label(
            graph=self.func,
            label= Tex(f"f(x{self.iter})"),
            x_val=self.xi,
            dot=True,
            direction=UR,
        )
         
        dot_i = always_redraw(lambda: ax.get_graph_label(
            graph=tangent,
            label = "",
            x_val=self.X.get_value(),
            dot=True,
            direction=UR,
            )
        )

        if self.iter ==0:
            #1)Create Axes
            self.play(Create(ax), run_time = 1)
            #2)Create func
            self.play(Create(self.func), run_time = 1)
            #3)Create label
            self.play(Create(VGroup(xi_label, fxi_label)), run_time = 1)
        else:
            #1-3) Create Axes, func, label
            self.add(VGroup(ax, self.func, xi_label, fxi_label))

        #4) Create tangent
        self.play(Create(VGroup(tangent, dot_i)), run_time = 1)
        self.wait()
        #5) Move to the new point
        self.play(self.X.animate.set_value(self.xi_1), run_time = 1)
        self.wait()

        xi_1_label = always_redraw(lambda:ax.get_T_label(
            label= Tex(f"x{self.iter+1}"),
            x_val=self.X.get_value(),
            graph=self.func, 
        ))
        
        fxi_1_label = always_redraw(lambda:ax.get_graph_label(
            graph=self.func,
            label= Tex(f"f(x{self.iter+1})"),
            x_val=self.X.get_value(),
            dot=True,
            direction=UR,
            ))
        
        vg = always_redraw(lambda: VGroup(ax,self.func, xi_1_label,  fxi_1_label))
        # func.add(xi_1_label)
        # func.add(fxi_1_label)

        #6)Create label
        self.play(Create(VGroup(xi_1_label, fxi_1_label)), run_time = 1)
        self.wait()

        #7)Uncreate labels and tangent
        self.play(Uncreate(VGroup(xi_label, fxi_label, tangent)), run_time = 1)
        self.wait()

        yrange = self.calc_zoom(self.fxi_1)

        #8)Zoom-in
        ax.add_updater(self.update_axes)
        self.ystep.set_value(yrange[2])
        self.play(self.ymax.animate.set_value(yrange[1]), self.ymin.animate.set_value(yrange[0]), run_time = 3)
        self.wait()
        ax.remove_updater(self.update_axes)
        self.wait()