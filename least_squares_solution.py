from manim import *
import numpy as np
import subprocess

config.frame_rate = 60


class LeastSquaresSolution(Scene):
    def construct(self):
        title = Text("Least-Squares-Solution", font_size=40)
        self.play(Write(title))
        # Move title up so it doesn't overlap with the graph
        self.play(title.animate.to_edge(UP))
        self.wait(1)

        # Draw a plane
        plane = NumberPlane(
            x_range=[0, 6, 1],
            y_range=[0, 6, 1],
            axis_config={"stroke_width": 2},
            background_line_style={"stroke_opacity": 0.3},

        )
        self.play(Create(plane))

        # Generate some points
        points_array = np.array([[1, 2], [2, 2.5], [3, 3.5], [4, 4.7], [5, 5]])
        points = VGroup(*[
            Dot(plane.c2p(x, y), radius=0.08, color=WHITE)
            for x, y in points_array
        ])
        self.play(FadeIn(points))
        self.wait(2)

        # Show x vector and 1 vector
        x_vec = Arrow(start=plane.c2p(0, 0), end=plane.c2p(5, 0), color=RED, buff=0)
        one_vec = Arrow(start=plane.c2p(0, 0), end=plane.c2p(0, 5), color=BLUE, buff=0)
        self.play(GrowArrow(x_vec), GrowArrow(one_vec))
        x_v_text = Text("X Vector", font_size=20).next_to(x_vec.get_end(), DOWN)
        one_v_text = Text("1 Vector", font_size=20).next_to(one_vec.get_end(), LEFT)
        self.play(Write(x_v_text), Write(one_v_text))
        self.wait(2)

        # Show plane spanned by 1 vect and x vect
        spanned_plane = Polygon(
            plane.c2p(0, 0),
            plane.c2p(5, 0),
            plane.c2p(5, 5),
            plane.c2p(0, 5),
            color=GREEN,
            fill_opacity=0.3,
            stroke_width=0
        )
        self.play(FadeIn(spanned_plane))
        plane_text = Text("Plane Spanned by the X vector and the 1 Vector", font_size=20).to_edge(DOWN)
        self.play(Write(plane_text))
        self.wait(2)
        self.play(FadeOut(plane_text))

        # compute regression line
        x = np.column_stack((np.ones(len(points_array)), points_array[:, 0]))
        y = points_array[:, 1]
        beta = np.linalg.inv(x.T @ x) @ x.T @ y
        y_hat = x @ beta
        regression_line = Line(
            start=plane.c2p(points_array[0, 0], y_hat[0]),
            end=plane.c2p(points_array[-1, 0], y_hat[-1]),
            color=PURPLE,
            stroke_width=4
        )
        self.play(Create(regression_line))
        regression_text = Text("Regression Line", font_size=20).to_edge(DOWN)
        self.play(Write(regression_text))
        self.wait(2)

        self.play(FadeOut(Group(*self.mobjects)))


def render_manim():
    command = ["manim", "-p", "--renderer=cairo", "least_squares_solution.py", "LeastSquaresSolution"]
    subprocess.run(command)


if __name__ == "__main__":
    render_manim()