from manim import *
import numpy as np
import subprocess

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 60


class Conclusion(Scene):
    def construct(self):
        conclusion_text = Text("Thank You!", font_size=96)
        self.play(Write(conclusion_text), run_time=3)
        # Hopefully, this video has helped you understand a little bit about how linear regression works, and given you insight
        # into how using linear algebra in a higher dimension can help solve advanced problems.

        # Thank you for watching!
        self.wait(12)
        self.play(FadeOut(conclusion_text))
        self.wait(2)

def render_manim():
    command = ["manim", "-p", "--renderer=cairo", "conclusion.py", "Conclusion"]
    subprocess.run(command)

if __name__ == "__main__":
    render_manim()