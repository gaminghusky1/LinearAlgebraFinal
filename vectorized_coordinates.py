from manim import *
import numpy as np
import subprocess

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 30

def create_ordered_pair(x, y, x_color, y_color):
    point = VGroup(
        MathTex("("),
        MathTex(f"{x}", color=x_color),
        MathTex(","),
        MathTex(f"{y}", color=y_color),
        MathTex(")")
    ).arrange(RIGHT, buff=0.15)
    point[2].shift(DOWN * 0.15)
    return point

class VectorizedCoordinates(Scene):
    def construct(self):
        # Setting up for projections
        points = VGroup(
            create_ordered_pair("x_1", "y_1", BLUE, RED),
            create_ordered_pair("x_2", "y_2", BLUE, RED),
            create_ordered_pair("x_3", "y_3", BLUE, RED),
            MathTex("\\cdots"),
            create_ordered_pair("x_n", "y_n", BLUE, RED)
        ).arrange(RIGHT, buff=0.5)
        self.play(Write(points), run_time=4)
        self.wait(2)
        x_vector = MobjectMatrix(
            [[points[0][1].copy()], [points[1][1].copy()], [points[2][1].copy()], [MathTex(r"\vdots")], [points[4][1].copy()]],
            element_alignment_corner=ORIGIN
        ).shift(LEFT)
        y_vector = MobjectMatrix(
            [[points[0][3].copy()], [points[1][3].copy()], [points[2][3].copy()], [MathTex(r"\vdots")], [points[4][3].copy()]],
            element_alignment_corner=ORIGIN
        ).shift(RIGHT)

        self.play(TransformMatchingShapes(points, VGroup(x_vector, y_vector)))
        self.wait(2)
        self.play(FadeOut(x_vector), FadeOut(y_vector))
        self.wait(2)
        # For any one given x-value, the corresponding y-value will be predicted with the standard slope-intercept form:
        singular_equation = MathTex(r"\hat{y_i}=mx_i+b")
        self.play(Write(singular_equation), run_time=3)
        self.wait(2)
        # So, this equation can be expressed in vector form to predict all y-values at once:
        vector_equation = MathTex(r"\hat{y}=m\cdot\overrightarrow{x}+b\cdot\overrightarrow{1}")
        self.play(TransformMatchingShapes(singular_equation, vector_equation))
        self.wait(1)
        # From this equation, we can see that y-hat, the prediction, is really just a linear combination of the x-vector and a vector of n ones.
        # Thus, y-hat must lie on the plane spanned by the x-vector and the 1-vector.
        # Now, we already have some values of y and x, so we can use those to find values for m and b that make the linear combination as close as possible to y.
        # We can determine these values by finding the closest point to y on the plane spanned by 1 and x, which turns out to be the projection of y onto that plane.
        # But how do we project y onto a plane?
        self.play(FadeOut(vector_equation))
        self.wait(2)

def render_manim():
    command = ["manim", "-p", "--renderer=cairo", "vectorized_coordinates.py", "VectorizedCoordinates"]
    subprocess.run(command)

if __name__ == "__main__":
    render_manim()