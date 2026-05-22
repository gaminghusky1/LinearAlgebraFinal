from manim import *
import numpy as np
import subprocess

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 60

class RegressionMath(Scene):
    def construct(self):
        intro_text = Text("The Mathematics Behind Linear Regression", font_size=50)
        # Now, let's see how we can put all this knowledge together to actually find a regression line given a set of points mathematically.
        self.play(Write(intro_text, run_time=4))
        self.wait(8)
        self.play(FadeOut(intro_text, run_time=2))
        self.wait(0.5)

        # First, we have to compute the orthogonal bases for span(x, 1)

        # The first orthogonal basis can be found by using the technique we just showed, subtracting the component of x in the direction of 1 from itself,
        # or the projection of x onto the one vector.
        # If we substitute in the formula for projection, we can see that this projection is just the mean of x times the one vector. So the first
        # orthogonal basis, x hat, is just the
        # x vector minus the mean of x times the one vector. And since x hat is orthogonal to the one vector, we now have our two orthogonal bases,
        # x hat and the one vector.
        x_hat_equation = MathTex(r"\hat{x} = ", r"\overrightarrow{x} - \mathrm{proj}_{\overrightarrow{1}} (\overrightarrow{x})")
        x_hat_equation_extended = MathTex(r"= \overrightarrow{x} - \overrightarrow{1} \frac{\overrightarrow{1} \cdot \overrightarrow{x}}{\overrightarrow{1} \cdot\overrightarrow{1}}")
        x_hat_equation_extended_2 = MathTex("=", r"\overrightarrow{x}", "-", r"\bar{x}", r"\cdot\overrightarrow{1}")
        x_hat_equation_final = MathTex(r"\hat{x} = ", r"\overrightarrow{x}", "-", r"\bar{x}", r"\cdot\overrightarrow{1}")

        x_projection_equation = MathTex(r"\mathrm{proj}_{\hat{x}}(\overrightarrow{y}) =", r"\hat{x}\,", r"\frac{\hat{x}\cdot\overrightarrow{y}}{\hat{x}\cdot\hat{x}}")
        one_projection_equation = MathTex(r"\mathrm{proj}_{\overrightarrow{1}}(\overrightarrow{y}) = \overrightarrow{1} \frac{\overrightarrow{1} \cdot \overrightarrow{y}}{\overrightarrow{1} \cdot \overrightarrow{1}}", "=", r"\bar{y}", r"\cdot \overrightarrow{1}")

        x_hat_group = VGroup(x_hat_equation, x_hat_equation_extended, x_hat_equation_extended_2).arrange(DOWN).move_to(ORIGIN)

        total_group = VGroup(x_hat_equation_final, x_projection_equation, one_projection_equation).arrange(DOWN).move_to(ORIGIN)

        projection_group = VGroup(x_projection_equation, one_projection_equation)

        self.play(Write(x_hat_equation, run_time=2))
        self.wait(16.5)
        self.play(Write(x_hat_equation_extended, run_time=2))
        self.wait(1)
        self.play(Write(x_hat_equation_extended_2, run_time=2))

        self.wait(6)

        self.play(TransformMatchingTex(x_hat_group, x_hat_equation_final, run_time=1))

        # 45

        self.wait(15)

        # Now we can find the projection of y onto each of these orthogonal bases and then sum them to find the projection of y onto span(x, 1),
        # which gives us the y_hat that minimizes the sum squared error.
        # Its important that while we do this, we keep everything in terms of x-hat and the one vector, since in the end we don't just
        # want to find y-hat, we want to find y-hat as a linear combination of the x-vector and one vector in order to find our m and b coefficients.

        # After we substitute x-hat with the expression we found earlier, we can simplify the equation for y-hat into a linear
        # combination of the x-vector and the one vector. This gives us the formulas for the coefficients m and b directly.

        # 60

        self.play(Write(x_projection_equation, run_time=2))

        self.wait(1)

        self.play(Write(one_projection_equation, run_time=2))

        #65


        self.wait(1)

        #66

        y_hat_equation = MathTex(r"\hat{y} = ", r"\hat{x}\,", r"\frac{\hat{x}\cdot\overrightarrow{y}}{\hat{x}\cdot\hat{x}}", "+", r"\bar{y}", r"\cdot \overrightarrow{1}")
        y_hat_x_hat_group = VGroup(y_hat_equation, x_hat_equation_final)

        y_hat_extra_equation = MathTex(r"\hat{y} = ", "(", r"\overrightarrow{x}", "-", r"\bar{x}", r"\cdot \overrightarrow{1}", r")\,", r"\frac{\hat{x}\cdot\overrightarrow{y}}{\hat{x}\cdot\hat{x}}", "+", r"\bar{y}", r"\cdot \overrightarrow{1}")

        y_hat_extra_equation_expanded = MathTex(r"\hat{y} = ", r"\overrightarrow{x}", r"\frac{\hat{x}\cdot\overrightarrow{y}}{\hat{x}\cdot\hat{x}}", "-", r"\bar{x}", r"\frac{\hat{x}\cdot\overrightarrow{y}}{\hat{x}\cdot\hat{x}}", r"\cdot \overrightarrow{1}", "+", r"\bar{y}", r"\cdot \overrightarrow{1}")

        y_hat_extra_expanded = MathTex(r"\hat{y} = ", "(", r"\frac{\hat{x}\cdot\overrightarrow{y}}{\hat{x}\cdot\hat{x}}", ")", r"\cdot", r"\overrightarrow{x}", r"-(", r"\bar{x}", r"\frac{\hat{x}\cdot\overrightarrow{y}}{\hat{x}\cdot\hat{x}}", "-", r"\bar{y}", ")", r"\cdot \overrightarrow{1}")

        self.play(TransformMatchingTex(projection_group, y_hat_equation, run_time=2))

        # 68

        self.wait(22)

        self.play(TransformMatchingTex(y_hat_x_hat_group, y_hat_extra_equation, run_time=2))

        self.wait(1)

        self.play(TransformMatchingTex(y_hat_extra_equation, y_hat_extra_equation_expanded, run_time=2))

        self.wait(1)

        self.play(TransformMatchingTex(y_hat_extra_equation_expanded, y_hat_extra_expanded, run_time=2))

        self.wait(2)

        self.add(y_hat_extra_expanded)

        # --- Targets (split so we can target subparts) ---
        m_equation = MathTex("m", "=", r"\frac{\hat{x}\cdot\overrightarrow{y}}{\hat{x}\cdot\hat{x}}")
        b_equation = MathTex("b", "=", r"-(", r"\bar{x}",
                             r"\frac{\hat{x}\cdot\overrightarrow{y}}{\hat{x}\cdot\hat{x}}",
                             "-", r"\bar{y}", ")")

        # --- Compute FINAL layout positions WITHOUT moving anything yet ---
        final_layout = VGroup(
            y_hat_extra_expanded.copy(),
            m_equation.copy(),
            b_equation.copy()
        ).arrange(DOWN, aligned_edge=LEFT)  # default buff
        final_layout.move_to(ORIGIN)

        # Move the real targets to their final positions (still not on screen)
        m_equation.move_to(final_layout[1])
        b_equation.move_to(final_layout[2])

        # --- Source pieces (from y_hat_extra_expanded) ---
        m_frac_src = y_hat_extra_expanded[2].copy()

        b_minus_src = y_hat_extra_expanded[6].copy()
        b_xbar_src = y_hat_extra_expanded[7].copy()
        b_frac_src = y_hat_extra_expanded[8].copy()
        b_plus_src = y_hat_extra_expanded[9].copy()
        b_ybar_src = y_hat_extra_expanded[10].copy()
        b_rparen_src = y_hat_extra_expanded[11].copy()

        # --- Target pieces ---
        m_prefix_tgt = VGroup(m_equation[0], m_equation[1])
        m_frac_tgt = m_equation[2]

        b_prefix_tgt = VGroup(b_equation[0], b_equation[1])
        b_minus_tgt = b_equation[2]
        b_xbar_tgt = b_equation[3]
        b_frac_tgt = b_equation[4]
        b_plus_tgt = b_equation[5]
        b_ybar_tgt = b_equation[6]
        b_rparen_tgt = b_equation[7]

        # --- Animate: y-hat slides up smoothly, while pieces move into m/b lines ---
        self.play(
            y_hat_extra_expanded.animate.move_to(final_layout[0]),

            Write(m_prefix_tgt),
            Write(b_prefix_tgt),

            ReplacementTransform(m_frac_src, m_frac_tgt),

            ReplacementTransform(b_minus_src, b_minus_tgt),
            ReplacementTransform(b_xbar_src, b_xbar_tgt),
            ReplacementTransform(b_frac_src, b_frac_tgt),
            ReplacementTransform(b_plus_src, b_plus_tgt),
            ReplacementTransform(b_ybar_src, b_ybar_tgt),
            ReplacementTransform(b_rparen_src, b_rparen_tgt),
            run_time=2
        )

        equation_group = VGroup(y_hat_extra_expanded, m_equation, b_equation)

        self.wait(7)

        self.play(FadeOut(equation_group))

        self.wait(1)


def render_manim():
    command = ["manim", "-p", "--renderer=cairo", "regression_math.py", "RegressionMath"]
    subprocess.run(command)

if __name__ == "__main__":
    render_manim()
