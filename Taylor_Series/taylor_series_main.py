from manim import *


class openingSzene(Scene):
    def construct(self):
        axes = Axes(
            x_range = [-2*np.pi, 2*np.pi+0.05, np.pi],
            y_range = [-1.5, 1.5, 0.5],
            x_length = 12,
            y_length = 6,
            axis_config = {"color": GREEN},
            #x_axis_config= {
            #    "numbers_to_include": np.arange(-3,3.01,1),
            #    "numbers_with_elongated_ticks": [ x for x in range(-2,3,2)]
            #},
            tips = True,
        )
        x_labels = [
            MathTex("-2\pi"), MathTex ("-\pi"), MathTex("0").add_background_rectangle(), MathTex("\pi"), MathTex("2\pi")
        ]
        for i in range(len(x_labels)):
            x_labels[i].next_to(np.array([ -6+3*i, 0, 0]), DOWN)
            self.add(x_labels[i])
            
        axes_labels = axes.get_axis_labels()
        sin_graph = axes.get_graph(lambda x: np.sin(x), color = BLUE)
        plot = VGroup(axes, sin_graph, axes_labels)
        self.add(plot)