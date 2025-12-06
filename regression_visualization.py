from manim import *
import subprocess
import numpy as np

config.pixel_width = 1920
config.pixel_height = 1080

class RegressionVisualization(ThreeDScene):
    def construct(self):
        # 3D axes from -20 to 20 on all axes
        axes = ThreeDAxes(
            x_range=(-20, 20, 5),
            y_range=(-20, 20, 5),
            z_range=(-20, 20, 5),
        )
        axes.add_coordinates()

        # Nice starting camera orientation
        self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES)

        # Vectors in the coordinate system of the axes
        origin = axes.c2p(0, 0, 0)
        end_v1 = axes.c2p(-10, -2, 3)
        end_v2 = axes.c2p(2, 4, 6)

        v1 = Arrow(
            start=origin,
            end=end_v1,
            color=RED,
        )
        v2 = Arrow(
            start=origin,
            end=end_v2,
            color=BLUE,
        )

        # Add everything
        self.play(Create(axes))
        self.wait(2)
        self.play(GrowArrow(v1))
        self.wait(1)
        self.play(GrowArrow(v2))

        # Spin the camera around the scene
        # This rotates about the Z-axis by changing theta continuously
        self.begin_ambient_camera_rotation(
            rate=0.3,  # radians per second
            about="theta",
        )

        # Let it spin for a bit
        self.wait(8)

        # Stop spinning
        self.stop_ambient_camera_rotation()
        self.wait(1)

def render_manim():
    command = ["manim", "-pql", "regression_visualization.py", "RegressionVisualization"]
    subprocess.run(command)

if __name__ == "__main__":
    render_manim()