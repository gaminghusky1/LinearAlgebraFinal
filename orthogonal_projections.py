from manim import *
import numpy as np
import subprocess

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 60

class OrthogonalProjections(ThreeDScene):
    def construct(self):
        # TODO: AFTER ORTHOGONAL BASES

        # Now, with this newfound knowledge on orthogonal bases, let's go back to our 3D example to see how we can
        # use them to find the projection of y onto the plane.
        axes = ThreeDAxes(
            x_range=(-10, 10, 1),
            y_range=(-10, 10, 1),
            z_range=(-10, 10, 1),
        )

        # Given vectors / point
        one = np.array([1.0, 1.0, 1.0])
        x = np.array([-3.0, -2.0, -1.0])
        y = np.array([2.0, 3.0, 7.0])

        # proj_1(x) and orthogonal component
        x_par = (np.dot(x, one) / np.dot(one, one)) * one  # proj_1(x)
        x_orth = x - x_par  # x - proj_1(x)

        # Plane morph parameter: 0 -> span{one, x}, 1 -> span{one, x_orth}
        basis_alpha = ValueTracker(0.0)

        def make_plane():
            a = basis_alpha.get_value()
            basis_x = (1 - a) * x + a * x_orth

            plane = NumberPlane(
                x_range=[-6, 6, 1],
                y_range=[-6, 6, 1],
                background_line_style={
                    "stroke_color": GREY,
                    "stroke_width": 1,
                    "stroke_opacity": 0.35,
                },
                axis_config={
                    "stroke_color": GREY,
                    "stroke_width": 3,
                    "stroke_opacity": 0.55,
                },
            )

            # Map (u,v) -> u*basis_x + v*one in R^3
            def map_to_span(p):
                u, v, _ = p
                world = u * basis_x + v * one
                return axes.c2p(*world)

            plane.apply_function(map_to_span)
            return plane

        plane = always_redraw(make_plane)

        # Camera + ambient rotation
        self.move_camera(phi=60 * DEGREES, theta=-45 * DEGREES, run_time=2)
        self.play(FadeIn(axes))
        self.begin_ambient_camera_rotation(rate=0.2)

        origin = axes.c2p(0, 0, 0)

        # Original vectors at the origin (no Create)
        x_vec = Arrow3D(origin, axes.c2p(*x), color=RED)
        one_vec = Arrow3D(origin, axes.c2p(*one), color=GREEN)
        self.add(x_vec, one_vec)
        self.play(DrawBorderThenFill(plane), run_time=2)
        self.wait(10)

        # Doing the same thing as before, and subtracting the projection of x onto 1 from x,
        # We obtain x-hat, which is orthogonal to 1 and makes the plane look much more familiar.

        # Show proj_1(x) as yellow (copy of x transforms into it)
        x_par_vec = Arrow3D(origin, axes.c2p(*x_par), color=YELLOW)
        self.play(TransformFromCopy(x_vec, x_par_vec), run_time=2)
        self.wait(3)

        # Show x - proj_1(x) as blue (copy of x transforms into it)
        # AND morph the plane's axes at the same time (x-basis -> x_orth-basis)
        x_orth_vec = Arrow3D(origin, axes.c2p(*x_orth), color=BLUE)
        self.play(
            basis_alpha.animate.set_value(1.0),
            TransformFromCopy(x_vec, x_orth_vec),
            run_time=3,
        )
        self.wait(4)

        # Fade out original x and proj_1(x)
        self.play(FadeOut(x_vec), FadeOut(x_par_vec), run_time=0.8)
        self.wait(0.3)

        # Fade in y point
        y_point = Dot3D(axes.c2p(*y), color=YELLOW, radius=0.06)
        self.play(FadeIn(y_point), run_time=0.8)
        self.wait(0.2)

        # Projections of y onto orthogonal bases: {one, x_orth}
        y_proj_one = (np.dot(y, one) / np.dot(one, one)) * one
        y_proj_orth = (np.dot(y, x_orth) / np.dot(x_orth, x_orth)) * x_orth
        y_proj_plane = y_proj_one + y_proj_orth

        # Dashed lines from y to each projection

        # Then, we project y onto each of the orthogonal basis vectors individually, which we already know how to do.
        dash_to_one = DashedLine(
            axes.c2p(*y),
            axes.c2p(*y_proj_one),
            dash_length=0.15,
            color=WHITE,
        )
        dash_to_orth = DashedLine(
            axes.c2p(*y),
            axes.c2p(*y_proj_orth),
            dash_length=0.15,
            color=WHITE,
        )

        # Pink projection vectors (initially both from origin)
        proj_one_vec = Arrow3D(origin, axes.c2p(*y_proj_one), color=PINK)
        proj_orth_vec = Arrow3D(origin, axes.c2p(*y_proj_orth), color=PINK)

        # After each dashed line, add the corresponding pink vector from the origin
        self.play(Create(dash_to_one), run_time=1.0)
        self.add(proj_one_vec)
        self.wait(0.2)

        self.play(Create(dash_to_orth), run_time=1.0)
        self.add(proj_orth_vec)
        self.wait(1)

        # Afterward, adding these projections together will give the projection of y onto the plane.

        # Note that this only works when the basis vectors are orthogonal, so they affect independent directions
        # and do not interfere or stack with each other.


        # Move the x_orth projection vector to the tip of the one projection vector
        proj_orth_shifted = Arrow3D(
            axes.c2p(*y_proj_one),
            axes.c2p(*(y_proj_one + y_proj_orth)),
            color=PINK,
        )
        self.play(Transform(proj_orth_vec, proj_orth_shifted), run_time=2)
        self.wait(2)

        # Optional: mark the final projected point
        final_dot = Dot3D(axes.c2p(*y_proj_plane), color=ORANGE, radius=0.06)
        self.play(FadeIn(final_dot), run_time=1)

        # Transform BOTH pink vectors together into the final pink vector to proj_plane
        final_template = Arrow3D(origin, axes.c2p(*y_proj_plane), color=PINK)
        self.play(
            FadeIn(final_template),
            FadeOut(proj_one_vec, proj_orth_vec),
            run_time=2,
        )

        self.wait(10)
        self.stop_ambient_camera_rotation()


def render_manim():
    command = ["manim", "-p", "--renderer=cairo", "--disable_caching", "--write_to_movie", "orthogonal_projections.py", "OrthogonalProjections"]
    subprocess.run(command)

if __name__ == "__main__":
    render_manim()


