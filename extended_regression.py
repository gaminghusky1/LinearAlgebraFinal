from manim import *
import numpy as np
import subprocess

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 60


class ExtendedRegression(Scene):
    def construct(self):
        # ---- Tune these ----
        row_buff   = 0.35   # horizontal spacing between eq, arrow, span
        row_gap    = 0.65   # vertical gap between the two rows (smaller = tighter)
        t_write_eq = 2.4
        t_shift_eq = 1.1
        t_write_rs = 1.8
        pause      = 0.7

        # ---- Objects ----
        linear_text = MathTex(r"\hat{y} = mx + b")
        linear_arrow = MathTex(r"\longrightarrow")
        linear_span_text = MathTex(r"\mathrm{span}(x, 1)")

        quadratic_text = MathTex(r"\hat{y} = m_1 x^2 + m_2 x + m_3")
        quadratic_arrow = MathTex(r"\longrightarrow")
        quadratic_span_text = MathTex(r"\mathrm{span}(x^2, x, 1)")

        def animate_row(eq, arrow, span, y_level):
            # Start: equation centered
            eq_start_pos = UP * y_level
            eq.move_to(eq_start_pos)

            # Compute the final layout FIRST (no snapping later)
            row_final = VGroup(eq.copy(), arrow.copy(), span.copy()).arrange(RIGHT, buff=row_buff)
            row_final.move_to(UP * y_level)  # row centered overall (so eq won’t go insanely left)

            eq_final_pos = row_final[0].get_center()
            arrow_final_pos = row_final[1].get_center()
            span_final_pos  = row_final[2].get_center()

            # Animate
            self.play(Write(eq), run_time=t_write_eq)
            self.wait(pause)

            self.play(eq.animate.move_to(eq_final_pos), run_time=t_shift_eq)

            arrow.move_to(arrow_final_pos)
            span.move_to(span_final_pos)
            self.play(Write(arrow), run_time=0.4)
            self.play(Write(span), run_time=t_write_rs)

            return VGroup(eq, arrow, span)

        # ---- Linear row ----
        linear_row = animate_row(linear_text, linear_arrow, linear_span_text, y_level=0.0)

        # Shift it up a bit (smaller vertical spacing)
        self.wait(0.4)
        self.play(linear_row.animate.shift(UP * row_gap), run_time=0.8)

        # ---- Quadratic row (starts near center, slightly below) ----
        quadratic_row = animate_row(quadratic_text, quadratic_arrow, quadratic_span_text, y_level=-0.25)

        self.wait(1)

        self.play(FadeOut(linear_row, run_time=0.5), FadeOut(quadratic_row, run_time=0.5))
        self.wait(0.5)

        # Show regressions
        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": GREY,
                "stroke_width": 1,
                "stroke_opacity": 0.4,
            },
            axis_config={"stroke_width": 3},
        )

        self.play(Create(plane), run_time=2)

        x_values = np.linspace(-4, 4, 9)
        base_y = np.array([-3.6, 0.7, -0.8, 0.5, 0.0, 0.9, -1.0, 3.1, 3.5])
        amplitudes = np.array([1.6, 0.35, 0.5, 0.25, 0.4, 0.3, 0.45, 2.5, 0.55])
        phases = np.array([0.0, 0.7, 1.2, 1.8, 2.4, 3.0, 3.4, 4.1, 4.7])

        t_tracker = ValueTracker(0.0)

        def current_y_values():
            t = t_tracker.get_value()
            return base_y + amplitudes * np.sin(t + phases)

        def current_coeffs():
            return np.polyfit(x_values, current_y_values(), 3)

        # Place dots at updater-consistent positions (t=0)
        y0 = current_y_values()

        dots = VGroup(*[
            Dot(plane.c2p(x, y), radius=0.06)
            for x, y in zip(x_values, y0)
        ])

        def dot_updater(mob, x, amp, phase, base):
            t = t_tracker.get_value()
            y = base + amp * np.sin(t + phase)
            mob.move_to(plane.c2p(x, y))

        for dot, x, amp, phase, base in zip(dots, x_values, amplitudes, phases, base_y):
            dot.add_updater(lambda m, x=x, amp=amp, phase=phase, base=base:
                            dot_updater(m, x, amp, phase, base))

        self.play(AnimationGroup(*[FadeIn(dot) for dot in dots], lag_ratio=0.08), run_time=2)

        regression_curve = always_redraw(
            lambda: plane.plot(
                lambda x: np.polyval(current_coeffs(), x),
                x_range=[x_values.min(), x_values.max()],
                color=YELLOW,
            )
        )
        self.play(Create(regression_curve), run_time=2)

        def build_equation(coeffs):
            cleaned = [0.0 if abs(c) < 1e-4 else c for c in coeffs]
            a, b, c, d = cleaned

            parts = []
            for idx, (coeff, power) in enumerate([(a, 3), (b, 2), (c, 1), (d, 0)]):
                sign = "-" if coeff < 0 else "+"
                value = abs(coeff)

                if power == 0:
                    term = f"{value:.2f}"
                elif power == 1:
                    term = f"{value:.2f}x"
                else:
                    term = f"{value:.2f}x^{{{power}}}"

                if idx == 0:
                    parts.append(("-" if coeff < 0 else "") + term)
                else:
                    parts.append(f" {sign} {term}")

            tex = "y = " + "".join(parts)
            return MathTex(tex).scale(0.8)

        equation = build_equation(current_coeffs()).to_edge(UP)
        eq_anchor = equation.get_center()
        self.play(FadeIn(equation), run_time=1.5)

        def equation_updater(mob):
            new = build_equation(current_coeffs()).to_edge(UP)
            new.move_to(eq_anchor)  # prevents equation from sliding with width changes
            mob.become(new)

        equation.add_updater(equation_updater)

        # ONE cycle + smooth => starts still, moves, ends still (no warbly multi-cycle)
        self.play(
            t_tracker.animate.set_value(2 * PI),
            run_time=8,
            rate_func=smooth,
        )

        self.wait(1)


def render_manim():
    command = ["manim", "-p", "--renderer=cairo", "extended_regression.py", "ExtendedRegression"]
    subprocess.run(command)


if __name__ == "__main__":
    render_manim()
