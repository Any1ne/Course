from manim import *
from sympy import *
import json
import math

# config.disable_caching = False
# config.pixel_height = 480
# config.pixel_width = 720

class Newtons(ZoomedScene):
    def __init__(self, **kwargs):
        ZoomedScene.__init__(
            self,
            zoom_factor=0.6,
            zoomed_display_height=4,
            zoomed_display_width=5,
            image_frame_stroke_width=20,
            zoomed_camera_config={ "default_frame_stroke_width": 3},
            zoomed_display_corner= [1, 0, 0.],
            zoomed_camera_frame_starting_position= [0., -6., 0.],
            zoom_activated=True,
            **kwargs
        )

    def construct(self):
        # self.zoomed_display.display_frame.set_opacity(opacity=1)
        # print("init")
        self.init()
        self.title = Title("Newton's Method")
        # self.zoomed_camera.frame.set_opacity(opacity=0)
        if self.iter ==0:
            self.play(Write(self.title))
            self.activate_zooming()
            # print("axes")
            self.Axes()
            # print("function")
            self.Function()
            # print("create_X")
            self.Labels()
        else:
            # print("continue_prev")
            self.Continue_prev()
        # print("tangent")
        self.Tangent()
        # print("update_x")
        self.Update_labels()
        # print("delete_old")
        self.Delete_old()
        # print("zoom_i")
        self.Zoom_in()

    def init(self):
        with open('config.json') as f:
            config = json.load(f)

        self.iter = config['Iteration']-1
        self.xi = config['xi']
        self.xi_1 = config['xi+1']

        if self.iter != 0:
            self.xi__1 = config['xi-1']
            self.fxi__1 = config['f(xi-1)']
        self.rest = config['Rest']
        self.fxi = config['f(xi)']
        self.fxi_1 = config['f(xi+1)']
        self.eps = config['Eps']

        x = symbols('x')
        self.func_expr = sympify(config['f(x)'])
        self.tang_expr = sympify(config['tangent'])
        self.X = ValueTracker(self.xi)
        self.Iter = ValueTracker(self.iter)
        
        xrange, self.scale_levelx = self.x_ranging()
        
        self.xmin = ValueTracker(xrange[0])
        self.xmax = ValueTracker(xrange[1])
        self.xstep = ValueTracker(xrange[2])

        yrange, self.scale_levely = self.y_ranging()
        self.ymin = ValueTracker(yrange[0])
        self.ymax = ValueTracker(yrange[1])
        self.ystep = ValueTracker(yrange[2])
        
    def Axes(self):
        self.ax = self.create_axes()
        self.zoomed_camera.frame.move_to(self.ax)
        self.play(Create(self.ax), run_time = 3)
        
    def create_axes(self):
        ax = Axes(x_range=[self.xmin.get_value(), self.xmax.get_value(), self.xstep.get_value()],
                  y_range=[self.ymin.get_value(), self.ymax.get_value(), self.ystep.get_value()],
                  x_length=7, y_length=6,
                  axis_config={"include_numbers": True, "font_size": 24}                                                
                  ).to_edge(LEFT, buff=0.5).shift(DOWN*0.5)
        return ax

    def Function(self):
        # self.newtitle = Title("Newton's Method: function")

        self.func_graph = self.create_function()
        self.clip(self.func_graph, self.ax)
        self.ax.add(self.func_graph)
        
        self.play(Create(self.func_graph), run_time = 1)

        # self.play(*[Create(self.func), ReplacementTransform(self.title, self.newtitle)], run_time = 1)
        # self.title = self.newtitle

    def create_function(self):
        func = self.ax.plot(
            lambda x: self.function(x),  # TODO: filter none real numbers try sqrt() ValueError: math domain error
            x_range=[self.xmin.get_value(), self.xmax.get_value()],
            color=BLUE,
            use_smoothing = False)
        return func

    def function(self, x):
        res = self.func_expr.subs('x', x).evalf()
        if not isinstance(res, Float):
            if re(res)>0:
                res = self.ymax.get_value()+1
            else:
                res = self.ymin.get_value()-1

        return res

    def Labels(self):
        # self.newtitle = Title("Newton's Method: aproximation")

        self.xi_var, self.fxi_var = self.create_variables(self.iter)
        self.add(self.xi_var, self.fxi_var)

        self.xi_label, self.fxi_label = self.create_labels(self.iter)
        self.play(Create(VGroup(self.xi_label, self.fxi_label)), run_time = 3)

        # self.play(*[Create(VGroup(self.xi_label, self.fxi_label)), ReplacementTransform(self.title, self.newtitle)], run_time = 3)
        # self.title = self.newtitle
        self.play(self.zoomed_camera.frame.animate.move_to(self.fxi_label), run_time = 3)

    def create_variables(self, iter):
        x_var = Variable(self.X.get_value(), f'x{iter}', num_decimal_places=3
                         ).next_to(self.zoomed_display.display_frame, DOWN, buff=0.5)
        fx_var = Variable(self.func_expr.subs('x', self.X.get_value()).evalf(), f'f(x{iter})', num_decimal_places=3
                          ).next_to(x_var, DOWN, buff=0.5)
    
        return x_var, fx_var

    def create_labels (self, iter):
        xi_label = self.ax.get_T_label(
            x_val=self.X.get_value(),
            graph=self.func_graph, 
            label=Text(f"x{iter}", font_size = 16),
            triangle_size=0.15,
            triangle_color=YELLOW)

        fxi_label = self.ax.get_graph_label(
            graph=self.func_graph,
            label = "",
            x_val=self.X.get_value(),
            dot=True,
            direction=DR,
            dot_config= {"radius": 0.06, "color": ORANGE}
        )
        return xi_label, fxi_label

    def Tangent(self):
        # self.newtitle = Title("Newton's Method: tangent")
        self.tang = self.create_tangent()
        self.clip(self.tang, self.ax)
        self.dot_i = self.create_dot()

        self.play(Create(VGroup(self.tang, self.dot_i)), run_time = 3)

        # self.play(*[Create(VGroup(self.tang, self.dot_i)), ReplacementTransform(self.title, self.newtitle)], run_time = 3)
        # self.title = self.newtitle

    def create_tangent(self):
        tangent = self.ax.plot(
            lambda x: self.tang_expr.subs('x', x).evalf(),
            x_range=[self.xmin.get_value(), self.xmax.get_value()],
            color=RED)
        return tangent
        
    def create_dot(self):
        dot = self.ax.get_graph_label(
            graph=self.tang,
            label = "",
            x_val=self.X.get_value(),
            dot=True,
            dot_config= {"radius": 0.06, "color": ORANGE}
            )
        return dot
    
    def Update_labels(self):
        # self.newtitle = Title("Newton's Method: new aproximation")
        self.X.set_value(self.xi_1)

        self.dot_i_1 = self.create_dot()
        self.xi_1_label, self.fxi_1_label = self.create_labels(self.iter+1)
        self.xi_1_var, self.fxi_1_var = self.create_variables(self.iter+1)
        
        
        self.play(*[ReplacementTransform(self.dot_i, self.dot_i_1), self.xi_var.tracker.animate.set_value(self.xi_1), self.fxi_var.tracker.animate.set_value(self.fxi_1), self.zoomed_camera.frame.animate.move_to(self.dot_i_1)], run_time = 3)
        self.play(*[Uncreate(VGroup(self.xi_var, self.fxi_var)), Create(VGroup(self.xi_1_var, self.fxi_1_var))], run_time=1)
        # self.play(*[ReplacementTransform(self.dot_i, self.dot_i_1), ReplacementTransform(self.title, self.newtitle), self.zoomed_camera.frame.animate.move_to(self.dot_i_1)], run_time = 3)
        # self.title = self.newtitle
        self.Iter.increment_value(1)
        self.play(Create(VGroup(self.xi_1_label,self.fxi_1_label)), run_time = 3)
        self.play(self.zoomed_camera.frame.animate.move_to(self.fxi_1_label), run_time = 3)

    def Delete_old(self):
        g = VGroup(self.xi_label, self.fxi_label, self.dot_i, self.tang, self.dot_i_1)
        self.play(*[Uncreate(mob) for mob in g], run_time = 3)

    def Zoom_in(self):
        if self.fxi !=0:
            zoom = abs((self.fxi_1/self.fxi))/self.get_zoom_factor()
            zoom = max(0.5, min(zoom, 2))
            self.play(self.zoomed_camera.frame.animate.scale(zoom))

    def Continue_prev(self):
        #Continue from prev Zoom
        self.ax = self.create_axes()
        self.func_graph =  self.create_function()
        self.clip(self.func_graph, self.ax)

        self.xi_label, self.fxi_label = self.create_labels(self.iter)

        self.xi_var, self.fxi_var = self.create_variables(self.iter)
        
        # print("ZOOM FACTOR", self.get_zoom_factor())
        if self.fxi__1 !=0:
            zoom = abs((self.fxi/self.fxi__1))/self.get_zoom_factor()
            zoom = max(0.5, min(zoom, 2))
            self.zoomed_camera.frame.scale(zoom)
        
        # self.zoomed_camera.frame.set_opacity(opacity=0)
        self.zoomed_camera.frame.move_to(self.fxi_label)
        
        # print("ZOOM FACTOR", self.get_zoom_factor())
        self.activate_zooming()
        self.add(VGroup(self.title, self.ax, self.func_graph, self.xi_label, self.fxi_label, self.xi_var, self.fxi_var))

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
    
    def x_ranging(self, level=0):
        a = self.rest[0]
        b = self.rest[1]

        # smaller range
        if -self.eps <= self.fxi <= self.eps:
            a = self.xi-2*self.eps
            b = self.xi+2*self.eps
        else:      
            if a <= self.xi <= b and a <= self.xi_1 <= b:
                if self.xi < self.xi_1:
                    k1 =min(abs(self.fxi), 1)
                    k2 =min(abs(self.fxi_1), 1)
                    a = k1*a + (1-k1)*self.xi 
                    b = k2*b + (1-k2)*self.xi_1
                else:
                    k1 =min(abs(self.fxi_1), 1)
                    k2 =min(abs(self.fxi), 1)
                    a = k1*a + (1-k1)*self.xi_1 
                    b = k2*b + (1-k2)*self.xi       
            elif b< self.xi or b< self.xi_1:
                if self.xi < self.xi_1:
                    k1 =min(abs(self.fxi), 1)
                    a = k1*a + (1-k1)*self.xi 
                    b = self.xi_1
                else:
                    k1 =min(abs(self.fxi_1), 1)
                    a = k1*a + (1-k1)*self.xi_1 
                    b = self.xi
            elif self.xi<a or self.xi_1< a:
                if self.xi < self.xi_1:
                    k2 =min(abs(self.fxi_1), 1)
                    a = self.xi
                    b = k2*b + (1-k2)*self.xi_1
                else:
                    k2 =min(abs(self.fxi), 1)
                    a = self.xi_1
                    b = k2*b + (1-k2)*self.xi       

        scale, level = self.calculacte_scale(a, b)

        a -= scale
        b += scale
        
        xrange= [a, b, scale]
        # print ("xrange", xrange)
        return xrange, level

    def y_ranging(self, k=3, l=2, m=5, level=0):
        if -self.eps <= self.fxi <= self.eps:
            A = -2*self.eps
            B = 2*self.eps
        else:
            d = self.fxi/k
            A = (k+l)*d
            B = -m*d
            if A>B:
                temp = A
                A=B
                B=temp
            if B< self.fxi or B< self.fxi_1:
                if self.fxi < self.fxi_1:
                    B = self.fxi_1
                else:
                    B = self.fxi
            elif self.fxi<A or self.fxi_1< A:
                if self.fxi_1 < self.fxi:
                    A = self.fxi_1
                else:
                    A = self.fxi
            
        # print("A, B", A, B)
        scale, level = self.calculacte_scale(A, B)

        A -= scale
        B += scale
            
        yrange=[round(A, 5), round(B, 5), scale]
        return yrange, level
    
    def calculacte_scale(self, A, B, level=0):
        scale = 1

        # print(f"Restriction: [{A}, {B}]")
        if A>B:
            temp = A
            A=B
            B=temp
       
        flag = False
        while not flag:
            n_ticks = (B-A)//scale
            # print("A, B, scale", A, B, n_ticks)
            # print(f"Number of ticks: {n_ticks}")
            # print(f"Curent level of scale: {self.scale_level}\n")

            if n_ticks<5:
                # scale down
                if level % 3 == 2 :
                    scale*=0.4
                else:
                    scale *= 0.5
                    
                level -=1
            elif n_ticks>12:
                # scale up
                if level % 3 == 1 :
                    scale /=0.4
                else:
                    scale /= 0.5
                level +=1
            else:
                flag = True

        scale = round(scale, 7)
        if scale ==0:
            scale = 1e10
        
        return scale, level