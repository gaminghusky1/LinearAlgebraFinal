from manim import *
import numpy as np
import subprocess

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 60

class OrthogonalBases(Scene):
    def construct(self):
        # To easily find the projection of y onto the subspace spanned by 1 and x, we can first find the orthogonal bases for that subspace,
        # or two perpendicular vectors that lie in the subspace. Then, we can find the projection of y onto those vectors,
        # which we already know how to do, and then add those projections together to get the projection of y onto the subspace.
        # This only works because the vectors are perpendicular, which is why we need to find the orthogonal bases.

        ortho_bases_text = Text("Orthogonal Bases", font_size=64)
        self.play(Write(ortho_bases_text), run_time=3)
        self.wait(5)
        self.play(FadeOut(ortho_bases_text))

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

        self.play(GrowArrow(one_vector), run_time=2)
        self.play(FadeIn(one_vector_tex))
        self.wait(1)
        self.play(GrowArrow(x_vector), run_time=2)
        self.play(FadeIn(x_vector_tex))
        self.wait(2)

        one_line = DashedLine(
            start=plane.c2p(*(one * -5)),
            end=plane.c2p(*(one * 5)),
            color=GREEN,
        )

        self.play(TransformFromCopy(one_vector, one_line))
        self.wait(1)

        x_to_one_line = DashedLine(
            start=plane.c2p(*x),
            end=plane.c2p(*proj_one_x),
            color=GREY,
            dash_length=0.1,
        )

        self.play(Create(x_to_one_line), run_time=2)
        self.wait(2)

        proj_one_x_vector = Arrow(
            start=plane.c2p(0, 0),
            end=plane.c2p(*proj_one_x),
            color=YELLOW,
            buff=0,
        )

        proj_tex = MathTex(r"\text{proj}_{\overrightarrow{1}} \overrightarrow{x}", color=YELLOW, font_size=30).next_to(proj_one_x_vector.get_tip())

        self.play(TransformFromCopy(x_vector, proj_one_x_vector))
        self.play(FadeIn(proj_tex))
        self.wait(2)

        x_hat_vector = Arrow(
            start=plane.c2p(0, 0),
            end=plane.c2p(*x_hat),
            color=BLUE,
            buff=0,
        )

        x_hat_vector_tex = MathTex(r"\hat{x}", color=BLUE, font_size=30).next_to(x_hat_vector.get_tip())

        self.play(TransformFromCopy(x_vector, x_hat_vector))
        self.play(FadeIn(x_hat_vector_tex))

        self.play(FadeOut(x_vector, x_vector_tex, x_to_one_line, proj_one_x_vector, proj_tex))

        x_hat_line = DashedLine(
            start=plane.c2p(*(x_hat * -5)),
            end=plane.c2p(*(x_hat * 5)),
            color=BLUE,
        )

        self.play(TransformFromCopy(x_hat_vector, x_hat_line))

        self.wait(2)



def render_manim():
    command = ["manim", "-p", "--renderer=cairo", "orthogonal_bases.py", "OrthogonalBases"]
    subprocess.run(command)

if __name__ == "__main__":
    render_manim()
