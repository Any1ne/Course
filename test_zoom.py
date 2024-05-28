from manim import *
from sympy import *
import json
import math

class ChangingZoomScale(ZoomedScene):
    def __init__(self, **kwargs):
        ZoomedScene.__init__(
            self,
            zoom_factor=0.5,
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
        self.init()
        self.activate_zooming()
        self.zoomed_camera.frame.set_opacity(opacity=0)
        # self.zoomed_display.display_frame.set_opacity(opacity=1) 
        # self.activate_zooming()
        # self.activate_zooming(animate=False)
        self.axes()
        self.function()
        self.create_tangent()
        self.zoom()

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
    
    def function(self):
        self.func =  self.ax.plot(lambda x: self.func_expr.subs('x', x), x_range=[self.xmin.get_value(), self.xmax.get_value()], color=BLUE).set_stroke(width=1)
        self.clip(self.func, self.ax)
        self.ax.add(self.func)
        self.play(Create(self.func), run_time = 1)

    def create_axes(self, y_min, y_max, y_step):
        self.ax = Axes(x_range=[self.xmin.get_value(), self.xmax.get_value(), self.xstep],
                  y_range=[y_min, y_max, y_step],
                  y_axis_config={"include_numbers": True}).scale(0.5).to_edge(LEFT)
        return self.ax
    
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
    
    def create_tangent(self):
        self.tangent = self.ax.plot(lambda x:  self.tang_expr.subs('x', x), x_range=[-5, 5])
         
        self.dot_i = always_redraw(lambda: self.ax.get_graph_label(
            graph=self.tangent,
            label = "",
            x_val=self.X.get_value(),
            dot=True,
            direction=UR,
            )
        )

        self.fxi_label = self.ax.get_graph_label(
            graph=self.func,
            label = "",
            x_val=self.xi,
            dot=True,
            dot_config={"radius": 0.01},
            direction=UR,
        ).set_stroke(width=1)

        self.play(Create(self.fxi_label), run_time = 1)
        # self.play(Create(self.dot_i), run_time = 1)

    # def construct(self):
    #     dot = Dot().set_color(GREEN)
    #     sq = Circle(fill_opacity=1, radius=0.2).next_to(dot, RIGHT)
    #     self.add(dot, sq)
    #     self.wait(1)
    #     self.activate_zooming(animate=True)
    #     self.wait(1)
    #     self.play(dot.animate.shift(LEFT * 0.3))

    #     self.play(self.zoomed_camera.frame.animate.scale(4))
    #     self.play(self.zoomed_camera.frame.animate.shift(0.5 * DOWN))
    
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
            
            # scale = 10  (math.floor(math.log10((B-A)/10)))*5
            yrange=[round(A, 5), round(B, 5), 1]
            print(yrange)
            # print((B-A)/scale)
            return yrange
    
    def zoom(self):
        self.zoomed_camera.frame.move_to(self.dot_i)
        # self.activate_zooming()
        self.zoomed_camera.frame.zoom_factor=0.5
        # self.play(self.fxi_label.scale(0.5))
        self.play(self.zoomed_camera.frame.animate.scale(0.5))
        self.zoomed_display.display_frame.to_edge(RIGHT)