from manim import *
import numpy as np
import math
import functools

class Functiontypes(Scene):
    
    def construct(self):
        axes = Axes(
            x_range=[-10, 10.9, 1],
            y_range=[-7, 7.5, 1],
            x_length=10,
            y_length=7,
            axis_config={"color": GREEN, "tick_size": 0.1,"stroke_width": 2,},
            x_axis_config={
                "numbers_to_include": np.arange(-10, 10.1, 2),
                #"numbers_with_elongated_ticks": np.arange(-10, 10.01, 2),
            },
            y_axis_config={
                "numbers_to_include": np.arange(-6, 6.1, 2),
                #"numbers_with_elongated_ticks": np.arange(-6, 6.01, 2),
            },
            tips=True,
        )
        axes_labels = axes.get_axis_labels()
        self.play(Create(axes), Create(axes_labels))

        ### Ganzrationale Funktionen
        
        func_graphs = [
            axes.get_graph(
                lambda x: x**a,
                color = BLUE,
            )
            for a in range(1,6)
        ]
        func_terms = [
            MathTex("f(x) = x^{%s}"%(a))
            for a in range(1,6)
        ]
        graph = func_graphs[0]
        term = func_terms[0].set_color(BLUE).to_corner(UR)
        self.play(Create(graph), Write(term))
        self.wait()
        for i in range(1,5):
            self.play(Transform(graph, func_graphs[i]), Transform(term, func_terms[i].set_color(BLUE).to_corner(UR)))
            self.wait()
        self.play(FadeOut(graph), FadeOut(term))
        self.wait()

        ### (un)echt Gebrochenrationale Funktionen

        func_graphs = [
            VGroup(
                axes.get_graph(
                    lambda x: 1/x,
                    color = BLUE,
                    x_range=[-10,-0.15]
                ),
                axes.get_graph(
                    lambda x: 1/x,
                    color = BLUE,
                    x_range=[0.15,10]
                ),
            ),
            VGroup(
                axes.get_graph(
                    lambda x: 1/x**2,
                    color = BLUE,
                    x_range = [-10,-0.1],
                ),
                axes.get_graph(
                    lambda x: 1/x**2,
                    color = BLUE,
                    x_range = [0.1,10],
                ),
            ),
            axes.get_graph(
                lambda x: 3/(x**2+1),
                color = BLUE,
            ),
            VGroup(
                axes.get_graph(
                    lambda x: x/(x-1),
                    color = BLUE,
                    x_range = [-10,0.9]
                ),
                axes.get_graph(
                    lambda x: x/(x-1),
                    color = BLUE,
                    x_range = [1.1, 10]
                ),
            ),
            VGroup(
                axes.get_graph(
                    lambda x: (x**2-1)/(x-2),
                    color = BLUE,
                    x_range=[-10, 1.9]
                ),
                axes.get_graph(
                    lambda x: (x**2-1)/(x-2),
                    color = BLUE,
                    x_range=[2.1, 10]
                ),
            ),
            VGroup(
                axes.get_graph(
                    lambda x: (x-3)/(2-x),
                    color = BLUE,
                    x_range = [-10,1.9]
                ),
                axes.get_graph(
                    lambda x: (x-3)/(2-x),
                    color = BLUE,
                    x_range = [2.1, 10]
                ),
            ),
        ]
        func_terms = [
            MathTex(r"f(x)=\frac{1}{x}"),
            MathTex(r"f(x)=\frac{1}{x^{2}}"),
            MathTex(r"f(x)=\frac{3}{x^{2}+1}"),
            MathTex(r"f(x)=\frac{x}{x-1}"),
            MathTex(r"f(x)=\frac{x^{2}-1}{x-2}"),
            MathTex(r"f(x)=\frac{x-3}{2-x}"),
        ]
        graph = func_graphs[0]
        term = func_terms[0].set_color(BLUE).to_corner(UR)
        self.play(Write(term))
        self.wait()
        for i in range(1,len(func_graphs)):
            self.play(Transform(graph, func_graphs[i]), Transform(term, func_terms[i].set_color(BLUE).to_corner(UR)))
            self.wait()
        self.play(FadeOut(graph), FadeOut(term))
        self.wait()

        ### Trigonometrische Funktionenen

        func_graphs = [
            axes.get_graph(
                lambda x: np.sin(x),
                color = BLUE,
            ),
            axes.get_graph(
                lambda x: np.cos(x),
                color = BLUE,
            ),
            axes.get_graph(
                lambda x: np.tan(x),
                color = BLUE,
                #t_range = np.array([0,1,0.0001]),
                #discontinuities=[-7*np.pi/2, -5*np.pi/2, -3*np.pi/2, -np.pi/2,7*np.pi/2, 5*np.pi/2, 3*np.pi/2, np.pi/2]
            )
        ]
        func_terms = [
            MathTex(r"f(x) = sin(x)"),
            MathTex(r"f(x) = cos(x)"),
            MathTex(r"f(x) = tan(x)")
        ]
        graph = func_graphs[0]
        term = func_terms[0].set_color(BLUE).to_corner(UR)
        self.play(Write(term))
        self.wait()
        for i in range(1,len(func_graphs)-1):
            self.play(Transform(graph, func_graphs[i]), Transform(term, func_terms[i].set_color(BLUE).to_corner(UR)))
            self.wait()
        #self.play(FadeOut(graph), FadeOut(term))
        self.wait()

        ### Potenzfunktionen

        

