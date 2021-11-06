from manim import *
import math
import functools


def derivative(func, x, order=1, dx = 0.01):        #Wenn nichts anderes angegeben, wird die erste Ableitung mit dx = 0.01 zurückgegeben
    """n-te Ableitung einer Funktion an Stelle x mit dx von 0.01"""
    partial = [func(x + (i - order/2)*dx) for i in range(order+1)]
    while(len(partial) > 1):
        partial = [
            (partial[j+1] - partial[j])/dx
            for j in range(len(partial)-1)
        ]
    return(partial[0])


def taylor_approximation(func, term_count, center_point = 0):
    """Taylor Annäherung einer Funktion mit k Termen an Entwicklungsstelle a"""
    coefficients = [
        derivative(func, center_point,n)/math.factorial(n)
        for n in range(term_count +1)
    ]
    return lambda x: sum([
        coefficients[n]*(x-center_point)**n
        for n in range(term_count +1)
    ])

def taylorseries_cosine(x, degree):
    """Wert von x abhängig vom Grad der Annäherung"""
    return sum([(-1)**i*x**(2*i)/math.factorial(2*i) for i in range(degree)])

def taylorseries_sine(x, degree):
    """Wert von x abhängig vom Grad der Annäherung"""
    return sum([(-1)**i*x**(2*i+1)/math.factorial(2*i+1) for i in range(degree)])

def taylorseries_exp(x, degree):
    """Wert von x abhängig vom Grad der Annäherung"""
    return sum([x**i/math.factorial(i)])


class openingSzene(Scene):
    def construct(self):
        axes = Axes(
            x_range = [-5.5*np.pi, 5.5*np.pi, np.pi],
            y_range = [-3, 3, 0.5],
            x_length = 12,
            y_length = 6,
            axis_config = {"include_tip": True, "color": GREEN},
            y_axis_config = {"numbers_to_include": [2,1,0,-1,-2],
            "decimal_number_config": {"num_decimal_places": 0}},
            #x_axis_config= {
            #    "numbers_to_include": np.arange(-3,3.01,1),
            #    "numbers_with_elongated_ticks": [ x for x in range(-2,3,2)]
            #},
        )
        x_labels = [
            MathTex("-5\pi"),MathTex("-4\pi"),MathTex("-3\pi"), MathTex("-2\pi"), MathTex ("-\pi"), 
            MathTex("0"), 
            MathTex("\pi"), MathTex("2\pi"), MathTex("3\pi"), MathTex("4\pi"), MathTex("5\pi")
        ]
        plot = VGroup()
        for i in range(len(x_labels)):
            x_labels[i].add_background_rectangle().next_to(np.array([ -6 + 12/(11*np.pi) + (6-12/(11*np.pi))/5*i, 0, 0]), 0.5*DOWN).scale(0.7)
            plot = VGroup(plot, x_labels[i])
        axes_labels = axes.get_axis_labels()
        sin_graph = axes.get_graph(lambda x: np.sin(x), color = BLUE)
        sin_label = MathTex("f(x)=sin(x)").next_to(np.array([0.75, 1.5, 0])).set_color(BLUE)
        plot = VGroup(axes, sin_graph, axes_labels, plot) 
        self.play(FadeIn(plot))
        self.wait()
        self.play(Write(sin_label))

class cosapproximation(Scene):
    def construct(self):
        axes = Axes(
            x_range = [-2.2*np.pi, 2.2*np.pi, np.pi],
            y_range = [-2.5, 2.5],
            x_length = 13,
            y_length = 7,
            axis_config={"color": BLUE},
            y_axis_config={"include_numbers": True, "decimal_number_config": {"num_decimal_places": 0}},
            tips = True
        )
        self.add(axes)
        cos_graph = axes.get_graph(lambda x: taylorseries_cosine(x, 10), color = GREEN)
        self.add(cos_graph)

