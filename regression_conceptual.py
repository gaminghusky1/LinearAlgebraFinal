from manim import *
import numpy as np
import subprocess

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 60

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

class RegressionConceptual(Scene):
    def construct(self):
        # AFTER INTRO
        # Now, let's dive into the concepts behind how linear regression is performed.
        # Setting up for projections
        points = VGroup(
            create_ordered_pair("x_1", "y_1", BLUE, RED),
            create_ordered_pair("x_2", "y_2", BLUE, RED),
            create_ordered_pair("x_3", "y_3", BLUE, RED),
            MathTex("\\cdots"),
            create_ordered_pair("x_n", "y_n", BLUE, RED)
        ).arrange(RIGHT, buff=0.5)
        # Normally, we would write points like this, as a series of ordered pairs of x and y.
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
        # For linear regression, however, we'll want to separate the x's and y's into their own vectors, to help with the equations we will use.
        self.play(TransformMatchingShapes(points, VGroup(x_vector, y_vector)))
        self.wait(2)
        self.play(FadeOut(x_vector), FadeOut(y_vector))
        self.wait(2)

        singular_equation = MathTex(r"\hat{y_i}=mx_i+b")
        self.play(Write(singular_equation), run_time=3)
        self.wait(1)

        # As we can recall from algebra, a standard form for a line is y = mx + b, or slope-intercept form.
        # This is also how we will express the regression line equation.
        slope_intercept_text = Text("Slope-Intercept Form", font_size=48).to_edge(UP)
        self.play(Write(slope_intercept_text), run_time=2)
        self.wait(1)

        # The way we "predict" the y for a certain x using our regression line is by plugging that
        # x-value, x_i, into our slope-intercept form equation and solving for the result.
        # Then, the result, y-hat_i, is the y predicted by the regression line.
        # This equation here predicts a single y when given a single x.
        brace = Brace(singular_equation, DOWN)
        brace_text = brace.get_tex(r"\text{Predicts a singular } y\text{-value}")
        self.play(GrowFromCenter(brace), Write(brace_text), run_time=2)
        self.wait(2)

        self.play(FadeOut(brace, brace_text))

        vector_equation = MathTex(r"\hat{y}=", r"m\overrightarrow{x}+b\overrightarrow{1}")

        vector_equation.move_to(singular_equation.get_center())

        # Now, recall that we represented our x's and y's as vectors earlier.
        # Using those vectors, we can express the regression line equation in a vectorized form.
        self.play(
            TransformMatchingShapes(
                singular_equation,
                vector_equation,
            ),
            run_time=3
        )
        self.wait(1)

        # This equation now predicts all y-values at once, from a single given x-vector.
        brace = Brace(vector_equation, DOWN)
        brace_text = brace.get_tex(r"\text{Predicts all } y\text{-values at once}")
        self.play(GrowFromCenter(brace), Write(brace_text), run_time=2)
        self.wait(2)

        # We can also see from this equation that y-hat, the prediction, is a linear combination of the x-vector and a vector of n ones.
        linear_combo_brace = Brace(vector_equation[1], UP)
        linear_combo_text = linear_combo_brace.get_tex(r"\text{Linear Combination of } \overrightarrow{x} \text{ and } \overrightarrow{1}")
        self.play(GrowFromCenter(linear_combo_brace), Write(linear_combo_text), run_time=2)
        self.wait(10)
        # Thinking about this geometrically, this means that y-hat must lie on the plane spanned by the x-vector and the 1-vector.
        # Recall that our goal in linear regression is to find the best values for m and b, or the slope and y-intercept,
        # that will minimize the sum of squared errors between the y-values of the points and the y-values of the regression line predictions.
        # To do this, we can find the regression line prediction vector, y-hat, that's closest to the actual y-vector,
        # which will be the closest point to the y-vector on the plane spanned by x and 1.
        # Then, because y-hat lies on the plane spanned by x and 1, we can break it down into its components along the x-vector and 1-vector to get m and b.
        # Now, it turns out that the closest point to y on the plane spanned by x and 1 is actually the projection of y onto that plane.
        # Once we find this projection, we can then find m and b and complete our regression.
        # But how do we project y onto a plane?
        self.play(FadeOut(vector_equation, slope_intercept_text, brace, brace_text, linear_combo_brace, linear_combo_text))
        self.wait(2)

def render_manim():
    command = ["manim", "-p", "--renderer=cairo", "regression_conceptual.py", "RegressionConceptual"]
    subprocess.run(command)

if __name__ == "__main__":
    render_manim()