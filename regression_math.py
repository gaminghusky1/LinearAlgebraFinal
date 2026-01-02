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


class RegressionMath(ThreeDScene):
    def construct(self):
        # First, we need to create orthogonal bases for the plane:
        axes = ThreeDAxes(
            x_range=(-10, 10),
            y_range=(-10, 10),
            z_range=(-10, 10),
        )
        one = np.array([1, 1, 1])
        x = np.array([-3, -2, -1])
        x_par = (np.dot(x, one) / np.dot(one, one)) * one
        x_orthog = x - x_par

        self.play(FadeIn(axes))
        self.move_camera(
            phi=60 * DEGREES,
            theta=-45 * DEGREES,
            run_time=3
        )
        self.begin_ambient_camera_rotation(rate=0.2)

        x_scale = ValueTracker(1.0)
        one_scale = ValueTracker(1.0)

        # x vector from origin
        # x_vector_3d = Arrow3D(
        #         axes.c2p(0, 0, 0),
        #         axes.c2p(*x),
        #         color=RED,
        # )
        #
        # def x_vector_updater(arrow):
        #     arrow.put_start_and_end_on(
        #         axes.c2p(0, 0, 0),
        #         axes.c2p(*(x_scale.get_value() * x)),
        #         color=RED
        #     )
        #
        # # one vector whose base follows the tip of x
        # one_vector = Arrow3D(
        #         axes.c2p(*(x_scale.get_value() * x)),  # base at tip of x
        #         axes.c2p(*(x_scale.get_value() * x + one_scale.get_value() * one)),  # same direction as 'one'
        #         color=GREEN,
        # )
        #
        # def one_vector_updater(arrow):
        #     arrow.put_start_and_end_on(
        #         axes.c2p(*(x_scale.get_value() * x)),
        #         axes.c2p(*(x_scale.get_value() * x + one_scale.get_value() * one)),
        #         color=GREEN,
        #     )
        #
        # x_vector_3d.add_updater(x_vector_updater)
        # one_vector.add_updater(one_vector_updater)

        x_vector_3d = always_redraw(
            lambda: Arrow3D(
                axes.c2p(0, 0, 0),
                axes.c2p(*(x_scale.get_value() * x)),
                color=RED,
            )
        )

        # one vector whose base follows the tip of x
        one_vector = always_redraw(
            lambda: Arrow3D(
                axes.c2p(*(x_scale.get_value() * x)),  # base at tip of x
                axes.c2p(*(x_scale.get_value() * x + one_scale.get_value() * one)),
                color=GREEN,
            )
        )

        self.add(x_vector_3d, one_vector)

        x_scale_label = DecimalNumber(
            x_scale.get_value(),
            num_decimal_places=2,
        ).scale(0.5)

        def update_x_label(mob):
            tip = x_scale.get_value() * x
            mob.set_value(x_scale.get_value())
            mob.move_to(axes.c2p(*(tip / 2)) + 0.3 * UP)
            return mob

        x_scale_label.add_updater(update_x_label)
        self.add(x_scale_label)

        one_scale_label = DecimalNumber(
            one_scale.get_value(),
            num_decimal_places=2,
        ).scale(0.5)

        def update_one_label(mob):
            tip = x_scale.get_value() * x + one_scale.get_value() * one
            mob.set_value(one_scale.get_value())
            mob.move_to(axes.c2p(*tip) + 0.3 * UP)
            return mob

        one_scale_label.add_updater(update_one_label)
        self.add(one_scale_label)

        # scales = [
        #     (2.5, 5.0),
        #     (-2.5, -5.0),
        #     (2.5, -5.0),
        #     (-2.5, 5.0),
        #     (0, 6.0),
        #     (0, -6.0),
        #     (2.0, 0),
        #     (-2.0, 0),
        #     (0.5, 1.0),
        #     (-1.2, 2.5),
        # ]

        # span_text = MathTex(r"span({\overrightarrow{x}, \overrightarrow{1}})")
        # span_text.to_edge(UP, buff=0.15)
        # self.add(span_text)

        scales = [
            (1.0, -2.0),
            (2.0, -1.5),
            (0.4, 2.3),
            (1.5, 3.2),
            (-1.0, -3.5),
            (1.0, 1.0),
        ]

        dots = VGroup()
        for a, b in scales:
            self.play(
                x_scale.animate.set_value(a),
                one_scale.animate.set_value(b),
                run_time=0.5
            )
            new_pt = a * x + b * one
            dot = Dot3D(axes.c2p(*new_pt), color=WHITE, radius=0.04)
            dots.add(dot)
            self.play(FadeIn(dot), run_time=0.2)

        self.wait(2)

        # x_vector_3d.remove_updater(x_vector_updater)
        # one_vector.remove_updater(one_vector_updater)

        # self.play(
        #     x_vector_3d.animate.become(
        #         Arrow3D(
        #             axes.c2p(0, 0, 0),
        #             axes.c2p(*x),
        #             # buff=0,
        #             color=RED,
        #             # stroke_width=4
        #         )
        #     ),
        #     one_vector.animate.become(
        #         Arrow3D(
        #             axes.c2p(0, 0, 0),
        #             axes.c2p(*one),
        #             # buff=0,
        #             color=GREEN,
        #             # stroke_width=4
        #         )
        #     )
        # )

        x_par_vector = x_vector_3d.copy()

        self.play(x_par_vector.animate.become(
            Arrow3D(
                axes.c2p(0, 0, 0),
                axes.c2p(*x_par),
                # buff=0,
                color=YELLOW,
                # stroke_width=4
            )
        ))

        x_orthog_vector = x_vector_3d.copy()

        self.play(x_orthog_vector.animate.become(
            Arrow3D(
                axes.c2p(0, 0, 0),
                axes.c2p(*x_orthog),
                # buff=0,
                color=BLUE,
                # stroke_width=4
            )
        ))

        self.play(FadeOut(x_par_vector))

        plane = NumberPlane(
            # x_range=[-7, 7, 1],
            # y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": GREY,
                "stroke_width": 1,
                "stroke_opacity": 0.4
            },
            axis_config={"stroke_width": 4},
        )

        # normal = np.cross(one, x)
        # basis_matrix = np.column_stack([one / np.linalg.norm(one),
        #                                 x / np.linalg.norm(x),
        #                                 normal / np.linalg.norm(normal)])
        # plane.apply_matrix(basis_matrix)
        def map_to_span(p):
            u, v, z = p
            world = u * x_orthog + v * one      # in R^3
            return axes.c2p(*world)      # into the scene coords used by axes / Arrow3D / Dot3D

        plane.apply_function(map_to_span)

        self.play(Create(plane, run_time=1))
        self.play(FadeOut(dots))

        # Do projection
        y = np.array([2, 3, 7])
        y_point = Dot3D(axes.c2p(*y), color=YELLOW, radius=0.06)
        self.play(FadeIn(y_point))
        self.wait(1)

        # normal to span(x, 1)
        normal = np.cross(one, x)
        normal_unit = normal / np.linalg.norm(normal)

        proj_y = y - np.dot(y, normal_unit) * normal_unit

        proj_line = DashedLine(
            axes.c2p(*y),
            axes.c2p(*proj_y),
            dash_length=0.15
        )

        proj_dot = Dot3D(axes.c2p(*proj_y), color=BLUE, radius=0.06)

        self.play(Create(proj_line))
        self.play(FadeIn(proj_dot))
        self.wait(1)

        # Move the vectors x, 1 to the projection point
        A = np.column_stack([x, one])
        (a, b), *_ = np.linalg.lstsq(A, proj_y, rcond=None)

        self.play(
            x_scale.animate.set_value(a),
            one_scale.animate.set_value(b),
            run_time=2
        )

        self.wait(1)

        # Add labels to the left of the screen

        x_scale_label.remove_updater(update_x_label)
        one_scale_label.remove_updater(update_one_label)

        m_val = x_scale.get_value()
        b_val = one_scale.get_value()

        m_target = MathTex(r"m =", f"{m_val:.2f}").scale(0.7)
        b_target = MathTex(r"b =", f"{b_val:.2f}").scale(0.7)

        m_target.to_corner(UL).shift(RIGHT * 0.5 + DOWN * 0.5)
        b_target.next_to(m_target, DOWN, aligned_edge=LEFT, buff=0.3)

        self.play(
            Transform(x_scale_label, m_target),
            Transform(one_scale_label, b_target),
            run_time=1.5
        )

        self.add_fixed_in_frame_mobjects(x_scale_label, one_scale_label)

        self.wait(2)

        # x_par_vector = x_vector_3d.copy()
        #
        # self.wait(1)
        # self.play(FadeIn(plane))
        # self.play(one_vector.animate.become(
        #     Line(
        #         axes.c2p(*(one * -10)),
        #         axes.c2p(*(one * 10)),
        #         color=GREEN,
        #         stroke_width=4
        #     )
        # ))
        # self.wait(1)
        # self.play(x_par_vector.animate.become(
        #     Arrow3D(
        #         axes.c2p(0, 0, 0),
        #         axes.c2p(*x_par),
        #         # buff=0,
        #         color=YELLOW,
        #         # stroke_width=4
        #     )
        # ))
        # self.wait(1)
        # x_orthog = x - x_par
        # normal = np.cross(one, x_orthog)
        # basis_matrix_orthog = np.column_stack([one / np.linalg.norm(one),
        #                                 x_orthog / np.linalg.norm(x_orthog),
        #                                 normal / np.linalg.norm(normal)])
        # self.play(
        #     x_vector_3d.animate.become(
        #         Arrow3D(
        #             axes.c2p(0, 0, 0),
        #             axes.c2p(*x_orthog),
        #             # buff=0,
        #             color=RED,
        #             # stroke_width=4
        #         )
        #     ),
        #     plane.animate.apply_matrix(basis_matrix_orthog @ np.linalg.inv(basis_matrix))
        # )
        # self.play(FadeOut(x_par_vector))
        # self.wait(1)
        # x_orthog_norm = x_orthog / np.linalg.norm(x_orthog)
        # self.play(x_vector_3d.animate.become(
        #     Line(
        #         axes.c2p(*(x_orthog_norm * -20)),
        #         axes.c2p(*(x_orthog_norm * 20)),
        #         color=RED,
        #         stroke_width=4
        #     )
        # ))
        # Now that we have orthogonal bases for the plane, let's see why they are important.
        # Let's say that y doesn't lie on this plane, but the closest point to y is here.
        # Then, this would be the projection of y onto the one-vector, and this would be the projection of y onto the orthogonal basis we just created.
        # Now, because these bases are orthogonal, we can simply add up these projection vectors to get the vector to the point closest to y on the plane.
        # TODO: Add animation for projection of y onto plane spanned by 1 and x.
        self.wait(4)
        self.stop_ambient_camera_rotation()

def render_manim():
    command = ["manim", "-p", "--renderer=cairo", "regression_math.py", "RegressionMath"]
    subprocess.run(command)

if __name__ == "__main__":
    render_manim()