from manim import *
import numpy as np
import subprocess

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 60

class OrthogonalBases(Scene):
    def construct(self):
        # The first step to finding the projection of y onto the subspace spanned by 1 and x is to find orthogonal
        # bases for that subspace, or two perpendicular vectors that lie in the subspace.
        self.wait(6)

        # Let's see how we can do this with a simple example.
        ortho_bases_text = Text("Orthogonal Bases", font_size=64)
        self.play(Write(ortho_bases_text), run_time=3)
        self.wait(4)
        self.play(FadeOut(ortho_bases_text), run_time=1)

        plane = NumberPlane(
            background_line_style={
                "stroke_color": GREY,
                "stroke_width": 1,
                "stroke_opacity": 0.9
            },
            axis_config={
                "stroke_width": 4,
            },
        )

        self.play(DrawBorderThenFill(plane), run_time=2)
        # TODO: Show 1 and x vectors and then show finding x-hat from subtracting projection of x onto 1 from x
        x = np.array([1, 3])
        one = np.array([1, 1])

        proj_one_x = np.dot(x, one) / np.dot(one, one) * one

        x_hat = x - proj_one_x

        one_vector = Arrow(
            start=plane.c2p(0, 0),
            end=plane.c2p(*one),
            color=GREEN,
            buff=0,
        )
        one_vector_tex = MathTex(r"\overrightarrow{1}", color=GREEN, font_size=30).next_to(one_vector.get_tip())

        x_vector = Arrow(
            start=plane.c2p(0, 0),
            end=plane.c2p(*x),
            color=RED,
            buff=0,
        )


        x_vector_tex = MathTex(r"\overrightarrow{x}", color=RED, font_size=30).next_to(x_vector.get_tip())

        # Here, we have the one-vector, drawn in green, and an x-vector, drawn in red.
        self.play(GrowArrow(one_vector), run_time=2)
        self.play(FadeIn(one_vector_tex))
        self.wait(1)
        self.play(GrowArrow(x_vector), run_time=2)
        self.play(FadeIn(x_vector_tex))
        self.wait(1)

        one_line = DashedLine(
            start=plane.c2p(*(one * -5)),
            end=plane.c2p(*(one * 5)),
            color=GREEN,
        )

        self.play(TransformFromCopy(one_vector, one_line), run_time=1)
        self.wait(1)

        x_to_one_line = DashedLine(
            start=plane.c2p(*x),
            end=plane.c2p(*proj_one_x),
            color=GREY,
            dash_length=0.1,
        )

        # We will first find the projection of the x-vector onto the one-vector.
        self.play(Create(x_to_one_line), run_time=1.5)
        self.wait(0.5)

        proj_one_x_vector = Arrow(
            start=plane.c2p(0, 0),
            end=plane.c2p(*proj_one_x),
            color=YELLOW,
            buff=0,
        )

        proj_tex = MathTex(r"\mathrm{proj}_{\overrightarrow{1}} (\overrightarrow{x})", color=YELLOW, font_size=30).next_to(proj_one_x_vector.get_tip())

        self.play(TransformFromCopy(x_vector, proj_one_x_vector), run_time=1.5)
        self.play(FadeIn(proj_tex))
        self.wait(2)

        x_hat_vector = Arrow(
            start=plane.c2p(0, 0),
            end=plane.c2p(*x_hat),
            color=BLUE,
            buff=0,
        )

        x_hat_vector_tex = MathTex(r"\hat{x}", color=BLUE, font_size=30).next_to(x_hat_vector.get_tip())

        # And, as we learned in class, if we subtract this projection from the original x-vector, we are essentially
        # removing the component of the x-vector that is parallel to the one-vector, leaving us with only the
        # orthogonal component, which we will call x-hat.
        self.play(TransformFromCopy(x_vector, x_hat_vector), run_time=5)
        self.play(FadeIn(x_hat_vector_tex))

        self.wait(8)

        self.play(FadeOut(x_vector, x_vector_tex, x_to_one_line, proj_one_x_vector, proj_tex))

        x_hat_line = DashedLine(
            start=plane.c2p(*(x_hat * -5)),
            end=plane.c2p(*(x_hat * 5)),
            color=BLUE,
        )

        # Thus, by using the one-vector and this new x-hat vector, we have found two orthogonal bases for the subspace spanned by one and x.
        self.play(TransformFromCopy(x_hat_vector, x_hat_line), run_time=1)

        self.wait(9)



def render_manim():
    command = ["manim", "-p", "--renderer=cairo", "orthogonal_bases.py", "OrthogonalBases"]
    subprocess.run(command)

if __name__ == "__main__":
    render_manim()
