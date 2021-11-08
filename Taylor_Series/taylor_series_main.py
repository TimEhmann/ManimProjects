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
    return sum([(-1)**i*x**(2*i)/math.factorial(2*i) for i in range(degree + 1)])

def taylorseries_sine(x, degree):
    """Wert von x abhängig vom Grad der Annäherung"""
    return sum([(-1)**i*x**(2*i+1)/math.factorial(2*i+1) for i in range(degree + 1)])

def taylorseries_exp(x, degree):
    """Wert von x abhängig vom Grad der Annäherung"""
    return sum([x**i/math.factorial(i) for i in range(degree + 1)])


class openingSzene(Scene):
    def construct(self):
        axes = Axes(
            x_range = [-5.5*np.pi, 5.5*np.pi, np.pi],
            y_range = [-3, 3, 0.5],
            x_length = 12,
            y_length = 6,
            axis_config = {"include_tip": True, "color": BLUE},
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
            x_labels[i].add_background_rectangle().next_to(np.array([ 5*(-6 + 12/(11*np.pi) + (6-12/(11*np.pi))/5*i), 0, 0]), 0.5*DOWN).scale(0.7)
            plot = VGroup(x_labels[i], plot)
        sin_graph = axes.get_graph(lambda x: taylorseries_sine(x,15), color = GREEN)
        sin_graph.apply_matrix([[5,0], [0,1]])
        sin_label = MathTex("f(x)=sin(x)").next_to(np.array([0.75, 1.5, 0])).set_color(GREEN)
        plot = VGroup(axes, sin_graph, plot)
        self.play(FadeIn(plot))
        self.wait()
        self.play(Write(sin_label))
        self.wait()
        self.play(
            x_labels[0].animate.shift((-6 + 12/(11*np.pi) + (6-12/(11*np.pi))/5*0 - x_labels[0].get_x())*RIGHT),
            x_labels[1].animate.shift((-6 + 12/(11*np.pi) + (6-12/(11*np.pi))/5*1 - x_labels[1].get_x())*RIGHT),
            x_labels[2].animate.shift((-6 + 12/(11*np.pi) + (6-12/(11*np.pi))/5*2 - x_labels[2].get_x())*RIGHT),
            x_labels[3].animate.shift((-6 + 12/(11*np.pi) + (6-12/(11*np.pi))/5*3 - x_labels[3].get_x())*RIGHT),
            x_labels[4].animate.shift((-6 + 12/(11*np.pi) + (6-12/(11*np.pi))/5*4 - x_labels[4].get_x())*RIGHT),
            x_labels[5].animate.shift((-6 + 12/(11*np.pi) + (6-12/(11*np.pi))/5*5 - x_labels[5].get_x())*RIGHT),
            x_labels[6].animate.shift((-6 + 12/(11*np.pi) + (6-12/(11*np.pi))/5*6 - x_labels[6].get_x())*RIGHT),
            x_labels[7].animate.shift((-6 + 12/(11*np.pi) + (6-12/(11*np.pi))/5*7 - x_labels[7].get_x())*RIGHT),
            x_labels[8].animate.shift((-6 + 12/(11*np.pi) + (6-12/(11*np.pi))/5*8 - x_labels[8].get_x())*RIGHT),
            x_labels[9].animate.shift((-6 + 12/(11*np.pi) + (6-12/(11*np.pi))/5*9 - x_labels[9].get_x())*RIGHT),
            x_labels[10].animate.shift((-6 + 12/(11*np.pi) + (6-12/(11*np.pi))/5*10 - x_labels[10].get_x())*RIGHT),
            ApplyMatrix([[0.2,0], [0,1]], sin_graph),
            run_time = 3,
        )
        self.wait()
        redbox = SurroundingRectangle(sin_label, buff = 0.1, color = RED)
        cross_1 = Line(start = redbox.get_corner(UL), end = redbox.get_corner(DR), color = RED)
        cross_2 = Line(start = redbox.get_corner(UR), end = redbox.get_corner(DL), color = RED)
        self.play(Create(redbox), GrowFromCenter(cross_1), GrowFromCenter(cross_2))

        


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
        plot = VGroup(axes)
        x_labels = [
            MathTex("-2\pi"), MathTex ("-\pi"), 
            MathTex(""), 
            MathTex("\pi"), MathTex("2\pi")
        ]
        for i in range(len(x_labels)):
            x_labels[i].add_background_rectangle().next_to(np.array([-26/4.4+i*13/4.4, 0, 0]), DOWN).scale(0.7)
            plot = VGroup(plot, x_labels[i])
        self.play(FadeIn(plot))
    
        def show_cosine_approximation_n_to_m(start_degree, finish_degree):
            for i in range(start_degree, finish_degree+1):
                if i == start_degree:
                    cos_appr = axes.get_graph(lambda x: taylorseries_cosine(x, i), color = GREEN)
                    self.play(Create(cos_appr))
                    self.wait()
                else:
                    next_iteration = axes.get_graph(lambda x: taylorseries_cosine(x, i), color = GREEN)
                    self.play(Transform(cos_appr, next_iteration))
                    self.wait()

        show_cosine_approximation_n_to_m(0,10)

class TestScene(Scene):
    def construct(self):
        axes = Axes(
            x_range = [-5.5*np.pi, 5.5*np.pi, np.pi],
            y_range = [-3, 3, 0.5],
            x_length = 12,
            y_length = 6,
            axis_config = {"include_tip": True, "color": BLUE},
            y_axis_config = {"numbers_to_include": [2,1,0,-1,-2],
            "decimal_number_config": {"num_decimal_places": 0}},
        )
        axes2 = Axes(
            x_range = [-2.2*np.pi, 2.2*np.pi, np.pi],
            y_range = [-3, 3, 0.5],
            x_length = 12,
            y_length = 6,
            axis_config = {"include_tip": True, "color": BLUE},
            y_axis_config = {"numbers_to_include": [2,1,0,-1,-2],
            "decimal_number_config": {"num_decimal_places": 0}},
        )
        g1 = axes.get_graph(lambda x: math.sin(x))
        stretch_matrix = [[5,0],[0,1]]
        self.play(ApplyMatrix(stretch_matrix, g1))
        self.play(FadeOut(g1))
        self.play(FadeIn(axes), FadeIn(g1))
        self.wait()
        stretch_matrix = [[0.2,0],[0,1]]
        self.play(Transform(axes, axes2), ApplyMatrix(stretch_matrix, g1))