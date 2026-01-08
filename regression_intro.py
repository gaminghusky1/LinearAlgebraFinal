from manim import *
import numpy as np
import subprocess

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 60

class RegressionIntro(Scene):
    def construct(self):
        # TODO: Need script for start
        # In this video, we will explore least-squares linear regression, first explaining what it is
        # and what it does, and then diving deep into the math behind how it works.

        intro_text = Text("Least-Squares Linear Regression", font_size=64)
        self.play(Write(intro_text), run_time=3)
        self.wait(2)
        self.play(FadeOut(intro_text))

        # Regression example
        data_points = np.array([
            [1, 1],
            [3, 3.5],
            [5, 4.5],
            [7, 3],
            [8.5, 6],
            [10, 5],
            [11.5, 6.5]
        ])

        slope, intercept = np.polyfit(data_points[:, 0], data_points[:, 1], 1)

        regression_function = lambda x: slope * x + intercept

        plane = NumberPlane(
            x_range=[-0.5, 12, 1],
            y_range=[-0.5, 7, 1],
            background_line_style={
                "stroke_color": GREY,
                "stroke_width": 1,
                "stroke_opacity": 0.9
            },
            axis_config={
                "stroke_width": 4,
                "include_numbers": True
            },
        )

        # Let's start with a plane
        self.play(DrawBorderThenFill(plane), run_time=2)

        point_group = VGroup()

        for point in data_points:
            point_group.add(Dot(plane.c2p(*point), color=YELLOW))

        # And add some data points
        self.wait(1)
        self.play(FadeIn(point_group), run_time=2)

        self.wait(3)

        # Draw Regression Line
        regression_line = plane.plot(regression_function, color=WHITE)

        # Least-squares linear regression is essentially finding the line that best fits a set of data points by
        # minimizing the squared distance between the points and the predicted line, which is also called the squared error.
        self.play(Create(regression_line), run_time=2)

        error_lines = VGroup()
        errors = VGroup()

        for point in data_points:
            y_hat = regression_function(point[0])
            curr_error_line = DashedLine(plane.c2p(*point), plane.c2p(point[0], y_hat), dash_length=0.15, color=RED)
            error = point[1] - y_hat
            if error > 0:
                curr_error = DecimalNumber(error, font_size=24).move_to(curr_error_line, aligned_edge=RIGHT).shift(LEFT * 0.25)
            else:
                curr_error = DecimalNumber(error, font_size=24).move_to(curr_error_line, aligned_edge=LEFT).shift(RIGHT * 0.25)
            errors.add(curr_error)
            error_lines.add(curr_error_line)
            self.play(Create(curr_error_line), run_time=0.5)
            self.play(FadeIn(curr_error), run_time=0.5)

        self.wait(5)

        # Animated terms squaring
        error_exponents = VGroup()
        for error in errors:
            exponent = MathTex("2", font_size=26)
            exponent.next_to(error, UR, buff=0.02)
            error_exponents.add(exponent)

        self.play(*[FadeIn(exp) for exp in error_exponents], run_time=1.5)

        # You can see from this calculation that the sum squared error for this regression line is ....
        squared_errors = VGroup()
        square_transforms = []
        for error, exponent in zip(errors, error_exponents):
            squared_value = np.round(error.get_value() ** 2, 2)
            squared_decimal = DecimalNumber(
                squared_value,
                num_decimal_places=2,
                font_size=24
            ).move_to(error.get_center())
            squared_errors.add(squared_decimal)
            square_transforms.append(ReplacementTransform(VGroup(error, exponent), squared_decimal))

        self.play(LaggedStart(*square_transforms, lag_ratio=0.15), run_time=2)
        errors = squared_errors

        graph_group = VGroup(plane, point_group, regression_line, error_lines, errors)
        self.play(graph_group.animate.scale(0.65).to_edge(DOWN), run_time=2)
        self.wait(2)

        # Animate squared terms moving to the top of the screen and summing
        desired_font_size = 44
        scale_factor = desired_font_size / 24
        errors.generate_target()
        errors.target.arrange(RIGHT, buff=0.6)
        errors.target.scale(scale_factor)
        errors.target.next_to(graph_group, UP, buff=0.5)
        self.play(MoveToTarget(errors), run_time=2)

        # We can show that this is the minimum squared error by moving the regression line slightly in either direction
        # and observing that the error increases no matter how we change it.
        plus_signs = VGroup()
        for left_error, right_error in zip(errors[:-1], errors[1:]):
            plus = MathTex("+", font_size=desired_font_size)
            midpoint = (left_error.get_right() + right_error.get_left()) / 2
            plus.move_to(midpoint)
            plus_signs.add(plus)
        self.play(*[FadeIn(symbol) for symbol in plus_signs], run_time=0.8)

        equals_sign = MathTex("=", font_size=desired_font_size)
        equals_sign.next_to(errors[-1], RIGHT, buff=0.3)
        equals_sign.set_opacity(0)
        self.add(equals_sign)

        sse_value = np.round(sum(error.get_value() for error in errors), 2)
        sse_decimal = DecimalNumber(
            sse_value,
            num_decimal_places=2,
            font_size=desired_font_size
        )
        sse_decimal.next_to(equals_sign, RIGHT, buff=0.3)
        sse_decimal.set_opacity(0)
        self.add(sse_decimal)

        left_expression = VGroup(*errors, *plus_signs)
        equation_group = VGroup(left_expression, equals_sign, sse_decimal)
        self.play(equation_group.animate.move_to(errors.get_center()), run_time=0.8)

        self.play(equals_sign.animate.set_opacity(1), run_time=0.6)

        self.wait(1)

        self.remove(sse_decimal)
        sse_decimal.set_opacity(1)
        self.play(TransformFromCopy(left_expression, sse_decimal), run_time=2)
        self.wait(2)


        mse_func = MathTex("SSE = \\sum_{i=1}^{n} (y_i - \\hat{y}_i)^2", font_size=36).to_edge(UP)

        self.play(Write(mse_func), run_time=1)


        x_mean = float(np.mean(data_points[:, 0]))
        y_mean = float(np.mean(data_points[:, 1]))

        m = ValueTracker(float(slope))

        def b_of(m_val: float) -> float:
            return y_mean - m_val * x_mean

        # Replace the (static) regression line with a dynamic one
        self.remove(regression_line)
        regression_line_dyn = always_redraw(
            lambda: plane.plot(
                lambda x: m.get_value() * x + b_of(m.get_value()),
                color=WHITE
            )
        )
        self.add(regression_line_dyn)

        # Replace static error lines with dynamic ones
        self.remove(error_lines)
        error_lines_dyn = VGroup(*[
            always_redraw(
                lambda p=p: DashedLine(
                    plane.c2p(p[0], p[1]),
                    plane.c2p(p[0], m.get_value() * p[0] + b_of(m.get_value())),
                    dash_length=0.15,
                    color=RED
                )
            )
            for p in data_points
        ])
        self.add(error_lines_dyn)

        # Update each squared error number (the ones at the top)
        for term, p in zip(errors, data_points):
            term.add_updater(
                lambda mob, p=p: mob.set_value(
                    (p[1] - (m.get_value() * p[0] + b_of(m.get_value()))) ** 2
                )
            )

        # Update SSE (sum of squared errors)
        sse_decimal.add_updater(
            lambda mob: mob.set_value(
                sum(
                    (p[1] - (m.get_value() * p[0] + b_of(m.get_value()))) ** 2
                    for p in data_points
                )
            )
        )

        # Keep the expression nicely laid out as values change width
        expr_anchor = VGroup(*errors, *plus_signs, equals_sign, sse_decimal).get_center()

        expression_all = VGroup(*errors, *plus_signs, equals_sign, sse_decimal)

        def layout_expr(_mob):
            errors.arrange(RIGHT, buff=0.6)
            for i, plus in enumerate(plus_signs):
                plus.move_to((errors[i].get_right() + errors[i + 1].get_left()) / 2)
            equals_sign.next_to(errors[-1], RIGHT, buff=0.3)
            sse_decimal.next_to(equals_sign, RIGHT, buff=0.3)
            expression_all.move_to(expr_anchor)

        expression_all.add_updater(layout_expr)

        # Wiggle the slope up/down and show SSE change (higher away from optimum)
        delta = 0.25
        self.play(m.animate.set_value(slope + delta), run_time=1.6)
        self.play(m.animate.set_value(slope - delta), run_time=2.0)
        self.play(m.animate.set_value(slope), run_time=1.6)
        self.wait(1)

        # (Optional) cleanup: stop live updates if you continue animating other things
        expression_all.remove_updater(layout_expr)
        for term in errors:
            term.clear_updaters()
        sse_decimal.clear_updaters()



def render_manim():
    command = ["manim", "-p", "--renderer=cairo", "regression_intro.py", "RegressionIntro"]
    subprocess.run(command)

if __name__ == "__main__":
    render_manim()
