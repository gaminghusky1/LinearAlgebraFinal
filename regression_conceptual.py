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
        self.wait(5)
        points = VGroup(
            create_ordered_pair("x_1", "y_1", BLUE, RED),
            create_ordered_pair("x_2", "y_2", BLUE, RED),
            create_ordered_pair("x_3", "y_3", BLUE, RED),
            MathTex("\\cdots"),
            create_ordered_pair("x_n", "y_n", BLUE, RED)
        ).arrange(RIGHT, buff=0.5)
        # Normally, when we think of a set of points, we see them as a series of ordered pairs of x's and y's.
        self.play(Write(points), run_time=4)
        self.wait(2)
        x_vector = MobjectMatrix(
            [[points[0][1].copy()], [points[1][1].copy()], [points[2][1].copy()], [MathTex(r"\vdots")],
             [points[4][1].copy()]],
            element_alignment_corner=ORIGIN
        ).shift(LEFT)
        y_vector = MobjectMatrix(
            [[points[0][3].copy()], [points[1][3].copy()], [points[2][3].copy()], [MathTex(r"\vdots")],
             [points[4][3].copy()]],
            element_alignment_corner=ORIGIN
        ).shift(RIGHT)
        # For linear regression, however, we'll want to separate the x's and y's into their own vectors. This will help with the equations we will use later on.
        self.play(TransformMatchingShapes(points, VGroup(x_vector, y_vector)), run_time=5)
        self.wait(3)
        self.play(FadeOut(x_vector), FadeOut(y_vector), run_time=1)
        self.wait(3)

        singular_equation = MathTex(r"\hat{y_i}=mx_i+b")
        self.play(Write(singular_equation), run_time=3)
        self.wait(1)

        # As we can recall from algebra, a standard form for a line is y = mx + b, or slope-intercept form.
        # This is also how we will express the regression line equation.
        slope_intercept_text = Text("Slope-Intercept Form", font_size=48).to_edge(UP)
        self.play(Write(slope_intercept_text), run_time=2)
        self.wait(22)

        # The way we "predict" the y for a certain x is by using our regression line equation, plugging an
        # x-value, x_i, into the equation and solving for the result.
        # Then, the result, y-hat_i, is the y-value predicted by the regression line.
        # The equation shown on screen right now predicts a single y when given a single x.
        brace = Brace(singular_equation, DOWN)
        brace_text = brace.get_tex(r"\text{Predicts a singular } y\text{-value}")
        self.play(GrowFromCenter(brace), Write(brace_text), run_time=5)
        self.wait(5)

        self.play(FadeOut(brace, brace_text))

        vector_equation = MathTex(r"\hat{y}=", r"m", r"\overrightarrow{x}", r"+", r"b", r"\overrightarrow{1}")

        vector_equation.move_to(singular_equation.get_center())

        # Now, recall that we represented our x's and y's as vectors earlier.
        # Using those vectors, we can express the regression line equation in a vectorized form.
        self.play(
            TransformMatchingShapes(
                singular_equation,
                vector_equation,
            ),
            run_time=5
        )
        self.wait(1)

        # Our equation now predicts all y-values at once, from a single given x-vector.
        brace = Brace(vector_equation, DOWN)
        brace_text = brace.get_tex(r"\text{Predicts all } y\text{-values at once}")
        self.play(GrowFromCenter(brace), Write(brace_text), run_time=5)
        self.wait(6)

        # If we look closely, we can also see from this equation that y-hat, the prediction, is a linear combination of the x-vector and a vector of n ones.
        linear_combo_brace = Brace(vector_equation[1:], UP)
        linear_combo_text = linear_combo_brace.get_tex(
            r"\text{Linear Combination of } \overrightarrow{x} \text{ and } \overrightarrow{1}")
        self.play(GrowFromCenter(linear_combo_brace), Write(linear_combo_text), run_time=4)
        self.wait(2)
        # Thinking about this geometrically, this means that y-hat must lie on the plane spanned by the x-vector and the 1-vector.
        y_hat_span_eq = MathTex(r"\hat{y} \in", r"\mathrm{span}(\overrightarrow{x}, \overrightarrow{1})").next_to(
            vector_equation, DOWN * 6)
        self.play(Write(y_hat_span_eq[0]), run_time=2)
        x_and_1_copy = VGroup(vector_equation[2].copy(), vector_equation[5].copy())
        self.play(TransformMatchingShapes(x_and_1_copy, y_hat_span_eq[1]), run_time=3)
        self.wait(3)
        # Recall that our goal in linear regression is to find the values of m and b, or the slope and y-intercept of the regression line,
        # that will minimize the sum of squared errors between the y-values of the points and the y-values of the regression line predictions.
        self.play(Circumscribe(vector_equation[1]), run_time=1)
        self.play(Circumscribe(vector_equation[4]), run_time=1)
        self.wait(8)

        final_eq = VGroup(vector_equation, slope_intercept_text, brace, brace_text, linear_combo_brace,
                          linear_combo_text, y_hat_span_eq)

        self.play(FadeOut(final_eq), run_time=1)
        self.wait(2)

        # Now, the key insight on how to do this comes when we look at the formulas for the sum squared error and the distance
        # formula.
        mse_func = MathTex(r"\text{SSE} = \sum_{i=1}^{n} (y_i - \hat{y}_i)^2", font_size=42).to_edge(UP)
        distance_eq = MathTex(r"\text{Distance} = \sqrt{\sum_{i=1}^{n} (y_i - \hat{y}_i)^2}", font_size=42)

        equations_group = VGroup(mse_func, distance_eq).arrange(DOWN).move_to(ORIGIN)

        self.play(Write(mse_func), run_time=3)
        self.wait(1)
        self.play(Write(distance_eq), run_time=3)
        self.wait(21)

        # The formula for the distance between the y vector and the y-hat point is almost identical to the sum squared error,
        # except for the square root. But it turns out, when we're minimizing a value, the square root really doesn't matter
        # because it's an increasing function, so if we minimize the distance between y-hat and y, we will also minimize
        # the sum squared error.

        self.play(FadeOut(distance_eq), FadeOut(mse_func), run_time=1)
        self.wait(1)

        # So, to minimize the sum squared error we can find the y-hat that's closest to the actual y-vector,
        # and then break it down into its x and 1 components to find m and b.
        # Then, we'll have the slope and intercept of our regression line.

        # Now, to actually find that point on the plane spanned by 1 and x that's closest to the y-vector, we can simply just
        # project the y-vector onto that plane. This works because a projection gives the point on a plane that minimizes the
        # distance to another point.

        # Let's take a look at a visual example. -> regression_visualizatio

        self.play(FadeIn(final_eq), run_time=1)
        self.wait(34)


def render_manim():
    command = ["manim", "-p", "--renderer=cairo", "regression_conceptual.py", "RegressionConceptual"]
    subprocess.run(command)


if __name__ == "__main__":
    render_manim()