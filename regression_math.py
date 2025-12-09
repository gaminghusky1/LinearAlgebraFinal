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
        # # TODO: Need script for start
        # intro_text = Text("Least-Squares Linear Regression", font_size=64)
        # self.play(Write(intro_text), run_time=3)
        # self.wait(2)
        # self.play(FadeOut(intro_text))
        #
        # points = VGroup(
        #     create_ordered_pair("x_1", "y_1", BLUE, RED),
        #     create_ordered_pair("x_2", "y_2", BLUE, RED),
        #     create_ordered_pair("x_3", "y_3", BLUE, RED),
        #     MathTex("\\cdots"),
        #     create_ordered_pair("x_n", "y_n", BLUE, RED)
        # ).arrange(RIGHT, buff=0.5)
        # self.play(Write(points), run_time=4)
        # self.wait(2)
        # x_vector = MobjectMatrix(
        #     [[points[0][1].copy()], [points[1][1].copy()], [points[2][1].copy()], [MathTex(r"\vdots")], [points[4][1].copy()]],
        #     element_alignment_corner=ORIGIN
        # ).shift(LEFT)
        # y_vector = MobjectMatrix(
        #     [[points[0][3].copy()], [points[1][3].copy()], [points[2][3].copy()], [MathTex(r"\vdots")], [points[4][3].copy()]],
        #     element_alignment_corner=ORIGIN
        # ).shift(RIGHT)
        #
        # self.play(TransformMatchingShapes(points, VGroup(x_vector, y_vector)))
        # self.wait(2)
        # self.play(FadeOut(x_vector), FadeOut(y_vector))
        # self.wait(2)
        # # For any one given x-value, the corresponding y-value will be predicted with the standard slope-intercept form:
        # singular_equation = MathTex(r"\hat{y_i}=mx_i+b")
        # self.play(Write(singular_equation), run_time=3)
        # self.wait(2)
        # # So, this equation can be expressed in vector form to predict all y-values at once:
        # vector_equation = MathTex(r"\hat{y}=m\cdot\overrightarrow{x}+b\cdot\overrightarrow{1}")
        # self.play(TransformMatchingShapes(singular_equation, vector_equation))
        # self.wait(1)
        # # From this equation, we can see that y-hat, the prediction, is really just a linear combination of the x-vector and a vector of n ones.
        # # Thus, y-hat must lie on the plane spanned by the x-vector and the 1-vector.
        # # Now, we already have some values of y and x, so we can use those to find values for m and b that make the linear combination as close as possible to y.
        # # We can determine these values by finding the closest point to y on the plane spanned by 1 and x, which turns out to be the projection of y onto that plane.
        # # But how do we project y onto a plane?
        # self.play(FadeOut(vector_equation))
        # self.wait(2)
        # First, we need to create orthogonal bases for the plane:
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
        axes = ThreeDAxes(
            x_range=(-10, 10),
            y_range=(-10, 10),
            z_range=(-10, 10),
        )
        one = np.array([1, 1, 1])
        x = np.array([-3, -2, -1])
        normal = np.cross(one, x)
        basis_matrix = np.column_stack([one / np.linalg.norm(one),
                                        x / np.linalg.norm(x),
                                        normal / np.linalg.norm(normal)])
        plane.apply_matrix(basis_matrix)
        self.play(FadeIn(axes))
        self.move_camera(
            phi=60 * DEGREES,
            theta=-135 * DEGREES,
            run_time=3
        )
        self.begin_ambient_camera_rotation(rate=0.3)

        x_scale = ValueTracker(1.0)
        one_scale = ValueTracker(1.0)

        # x vector from origin
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
                axes.c2p(*(x_scale.get_value() * x + one_scale.get_value() * one)),  # same direction as 'one'
                color=GREEN,
            )
        )

        self.add(x_vector_3d, one_vector)

        scales = [
            (2.5, 5.0),
            (-2.5, -5.0),
            (2.5, -5.0),
            (-2.5, 5.0),
            (0, 6.0),
            (0, -6.0),
            (2.0, 0),
            (-2.0, 0),
            (0.5, 1.0),
            (-1.2, 2.5),
        ]

        # span_text = MathTex(r"span({\overrightarrow{x}, \overrightarrow{1}})")
        # span_text.to_edge(UP, buff=0.15)
        # self.add(span_text)

        for scale in scales:
            self.play(x_scale.animate.set_value(scale[0]), one_scale.animate.set_value(scale[1]), run_time=1)
            new_pt = scale[0] * x + scale[1] * one
            dot = Dot3D(axes.c2p(*new_pt), color=WHITE)
            self.play(FadeIn(dot), run_time=0.5)

        self.wait(2)

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
        # # Now that we have orthogonal bases for the plane, let's see why they are important.
        # # Let's say that y doesn't lie on this plane, but the closest point to y is here.
        # # Then, this would be the projection of y onto the one-vector, and this would be the projection of y onto the orthogonal basis we just created.
        # # Now, because these bases are orthogonal, we can simply add up these projection vectors to get the vector to the point closest to y on the plane.
        # # TODO: Add animation for projection of y onto plane spanned by 1 and x.
        # self.wait(4)
        # self.stop_ambient_camera_rotation()

def render_manim():
    command = ["manim", "-pql", "--renderer=opengl", "regression_math.py", "RegressionMath"]
    subprocess.run(command)

if __name__ == "__main__":
    render_manim()