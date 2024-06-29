from manim import *

class Manual(Scene):
    def construct(self):
        inst_text = (
            "1) Change and Update configuration\n"
            "2) Start rendering animation\n"
            "3) Watch results in videoplayer, infobox, or plot\n"
        )
        justified_text = MarkupText(inst_text, justify=True, font_size=32)

        title = Title("Manual")
        self.add(title,justified_text)