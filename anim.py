from manim import *
from sympy import *
import json

class Newtons(Scene):
    def construct(self):
        print("excelent")
        with open('config.json') as f:
            config = json.load(f)

        xi = config['xi']
        xi_1 = config['xi+1']
        iter = config['Iteration']

        x = symbols('x')
        func_expr = eval(config['f(x)'])
        tang_expr = eval(config['tangent'])


        ax = Axes()

        func = ax.plot(lambda x: func_expr.subs('x', x), x_range=[-5, 5], use_smoothing=False)
        tangent = ax.plot(lambda x:  tang_expr.subs('x', x), x_range=[-5, 5], use_smoothing=False)

        xi_label = ax.get_T_label(
            x_val=xi,
            graph=func, 
            label=Tex(f"x{iter}")
        )

        fxi_label = ax.get_graph_label(
            graph=func,
            label= Tex(f"f(x{iter})"),
            x_val=xi,
            dot=True,
            direction=UR,
        )

        X = ValueTracker(xi)
        
        dot_i = always_redraw(lambda: ax.get_graph_label(
            graph=tangent,
            label = "",
            x_val=X.get_value(),
            dot=True,
            direction=UR,
            )
        )

        if config['Iteration'] ==0:
            #Create Axes
            self.play(Create(ax), run_time = 3)
            #Create func
            self.play(Create(func), run_time = 3)
            #Configure axesxi_1
            self.play(Create(VGroup(xi_label, fxi_label)), run_time = 3)
        else:
            self.add(VGroup(ax, func, xi_label, fxi_label))

        self.play(Create(VGroup(tangent, dot_i)), run_time = 3)
        self.play(X.animate.set_value(xi_1), run_time = 3)
        self.wait()

        
        xi_1_label = ax.get_T_label(
            label= Tex(f"x{iter+1}"),
            x_val=X.get_value(),
            graph=func, 
        )

        fxi_1_label = always_redraw(lambda: ax.get_graph_label(
            graph=func,
            label= Tex(f"f(x{iter+1})"),
            x_val=X.get_value(),
            dot=True,
            direction=UR,
            )
        )

        self.play(Create(xi_1_label), run_time = 3)
        self.wait()

        self.play(Uncreate(VGroup(xi_label, fxi_label, tangent)), run_time = 3)
        self.wait()

        self.play(Create(fxi_1_label), run_time = 3)
        self.wait()