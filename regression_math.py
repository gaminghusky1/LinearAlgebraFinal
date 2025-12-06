from manim import *
import numpy as np
import subprocess

config.pixel_width = 1920
config.pixel_height = 1080


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


class RegressionMath(ThreeDScene):
    def construct(self):
        # TODO: Need script for start;
        intro_text = Text("Least-Squares Linear Regression", font_size=64)
        self.play(Write(intro_text), run_time=3)
        self.wait(2)
        self.play(FadeOut(intro_text))

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
        # First, we need to create orthogonal bases for the plane:
        plane = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": GREY,
                "stroke_width": 1,
                "stroke_opacity": 0.4
            },
            axis_config={"stroke_width": 4},
        )
        self.play(FadeIn(plane))
        one_vector = Arrow(
            plane.c2p(0, 0),
            plane.c2p(1, 1),
            buff=0,
            stroke_width=4,
            color=GREEN,
        )
        self.play(GrowArrow(one_vector))
        x_vector_2d = Arrow(
            plane.c2p(0, 0),
            plane.c2p(2, 3),
            buff=0,
            stroke_width=4,
            color=RED,
        )
        x_par = x_vector_2d.copy()
        self.play(GrowArrow(x_vector_2d))
        self.wait(1)
        self.play(one_vector.animate.become(
            Line(
                plane.c2p(-10, -10),
                plane.c2p(10, 10),
                color=GREEN,
                stroke_width=4
            )
        ))
        self.wait(1)
        self.play(x_par.animate.become(
            Arrow(
                plane.c2p(0, 0),
                plane.c2p(2.5, 2.5),
                buff=0,
                color=YELLOW,
                stroke_width=4
            )
        ))
        self.wait(1)
        self.play(x_vector_2d.animate.become(
            Arrow(
                plane.c2p(0, 0),
                plane.c2p(-0.5, 0.5),
                buff=0,
                color=RED,
                stroke_width=4
            )
        ))
        self.play(FadeOut(x_par))
        self.wait(1)
        self.play(x_vector_2d.animate.become(
            Line(
                plane.c2p(-10, 10),
                plane.c2p(10, -10),
                color=RED,
                stroke_width=4
            )
        ))
        # Now that we have orthogonal bases for the plane, let's see why they are important.
        # Let's say that y doesn't lie on this plane, but the closest point to y is here.
        # Then, this would be the projection of y onto the one-vector, and this would be the projection of y onto the orthogonal basis we just created.
        # Now, because these bases are orthogonal, we can simply add up these projection vectors to get the vector to the point closest to y on the plane.
        # TODO: Add animation for projection of y onto plane spanned by 1 and x.
        self.wait(2)

def render_manim():
    command = ["manim", "-pql", "regression_math.py", "RegressionMath"]
    subprocess.run(command)

if __name__ == "__main__":
    render_manim()