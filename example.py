from manim import *
import subprocess
import json

class PointMovingOnShapes(Scene):
    def construct(self):
        with open('config.json') as f:
            config = json.load(f)
        
        radius = config['radius']
        color = config['color']

        circle = Circle(radius=radius, color=color)

        dot = Dot()
        dot2 = dot.copy().shift(RIGHT)
        self.add(dot)

        line = Line([3, 0, 0], [5, 0, 0])
        self.add(line)

        self.play(GrowFromCenter(circle))
        self.play(Transform(dot, dot2))
        self.play(MoveAlongPath(dot, circle), run_time=2, rate_func=linear)
        self.play(Rotating(dot, about_point=[2, 0, 0]), run_time=1.5)
        self.wait()


