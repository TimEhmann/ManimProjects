import sympy
import math
import numpy as np

def f_deriv(f, x_val, n):
    x = sympy.symbols('x')
    f_n = f
    for _ in range(n):
        f_n = sympy.diff(f_n, x)
    return float(f_n.subs(x, x_val))

def taylor_approx_at_a(f, x, a, n_terms):
    val = 0.0
    a = float(a)
    x = float(x)
    for n in range(n_terms + 1):
        deriv_at_a = f_deriv(f, a, n)
        term = deriv_at_a / math.factorial(n) * (x - a)**n
        if abs(term) > 100:
            term = np.sign(term) * 100
        val += term
    if abs(val) > 5:
        return np.sign(val) * 5
    return val

from manim import *

class TaylorApproximationGraph(Scene):
    def construct(self):
        # Set up axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-1, 2, 0.5],
            x_length=10,
            y_length=5,
            axis_config={"include_numbers": True},
        ).to_edge(DOWN)

        labels = axes.get_axis_labels(x_label="x", y_label="f(x)")
        self.play(Create(axes), Write(labels))

        # Define symbolic function
        x_sym = sympy.symbols('x')
        f_expr = 1 / (1 + x_sym**2)  # Change to sympy.log(x_sym) if you want log(x)

        # Plot the original function
        original_func = lambda x: 1 / (1 + x**2)
        func_graph = axes.plot(original_func, x_range=[-4, 4], color=BLUE)
        func_label = axes.get_graph_label(func_graph, label="f(x)")

        self.play(Create(func_graph), Write(func_label))
        self.wait(1)

        # Animate Taylor Approximations with increasing terms
        a = 1  # Expansion point
        taylor_graphs = []
        colors = [ORANGE, GREEN, RED, YELLOW, PURPLE, MAROON]

        for i in range(1, 6):  # Increase the number of terms
            taylor_func = lambda x, i=i: taylor_approx_at_a(f_expr, x, a, i)
            graph = axes.plot(taylor_func, x_range=[-4, 4], color=colors[i % len(colors)])
            label = MathTex(f"T_{{{i}}}(x)").next_to(axes, UP).shift(LEFT * 3)

            if taylor_graphs:
                self.play(Transform(taylor_graphs[-1], graph), Transform(label_old, label))
                taylor_graphs[-1] = graph
            else:
                self.play(Create(graph), Write(label))
                taylor_graphs.append(graph)
            label_old = label
            self.wait(1)

        self.wait(2)