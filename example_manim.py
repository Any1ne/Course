from manim import *
import json
import os

config_name = 'config.json'

class PointMovingOnShapes(Scene):
    def construct(self):
        print("excelent")
        with open(config_name) as f:
            config = json.load(f)
        
        radius = 1
        color = "Blue"

        circle = Circle(radius=radius, color=color)

        dot = Dot()
        dot2 = dot.copy().shift(RIGHT)
        self.add(dot)

        line = Line([2, 0, 0], [5, 0, 0])
        self.add(line)

        self.play(GrowFromCenter(circle))
        self.play(Transform(dot, dot2))
        self.play(MoveAlongPath(dot, circle), run_time=2, rate_func=linear)
        self.play(Rotating(dot, about_point=[2, 0, 0]), run_time=1.5)
        self.wait()