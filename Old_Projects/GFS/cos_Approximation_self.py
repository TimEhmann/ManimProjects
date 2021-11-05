from manimlib.imports import *
#from big_ol_pile_of_manim_imports import *
import numpy as np
import functools

def derivative(func, x, n = 1, dx = 0.01):
    samples = [func(x + (k - n/2)*dx) for k in range(n+1)]
    while len(samples) > 1:
        samples = [
            (s_plus_dx - s)/dx
            for s, s_plus_dx in zip(samples, samples[1:])
        ]
    return samples[0]

def taylor_approximation(func, highest_term, center_point = 0):
    derivatives = [
        derivative(func, center_point, n = n)
        for n in range(highest_term + 1)
    ]
    coefficients = [
        d/math.factorial(n) 
        for n, d in enumerate(derivatives)
    ]
    return lambda x : sum([
        c*((x-center_point)**n) 
        for n, c in enumerate(coefficients)
    ])

class ExampleApproximation(GraphScene):
    CONFIG = {
        "function" : lambda x : np.exp(-x**2),
        "function_tex" : "e^{-x^2}", 
        "function_color" : BLUE,
        "order_sequence" : [0, 2, 4],
        "center_point" : 0,
        "approximation_terms" : ["1 ", "-x^2", "+\\frac{1}{2}x^4"],
        "approximation_color" : GREEN,
        "x_min" : -3,
        "x_max" : 3,
        "y_min" : -1,
        "y_max" : 2,
        "graph_origin" : DOWN + 2*LEFT,
    }
    def construct(self):
        self.setup_axes()
        func_graph = self.get_graph(
            self.function,
            self.function_color,
        )
        approx_graphs = [
            self.get_graph(
                taylor_approximation(self.function, n),
                self.approximation_color
            )
            for n in self.order_sequence
        ]

        near_text = TextMobject(
            "Near %s $= %d$"%(
                self.x_axis_label, self.center_point
            )
        )
        near_text.to_corner(UP + RIGHT)
        near_text.add_background_rectangle()
        equation = TexMobject(
            self.function_tex, 
            "\\approx",
            *self.approximation_terms
        )
        equation.next_to(near_text, DOWN, MED_LARGE_BUFF)
        equation.to_edge(RIGHT)
        near_text.next_to(equation, UP, MED_LARGE_BUFF)
        equation.set_color_by_tex(
            self.function_tex, self.function_color,
            substring = False
        )
        approx_terms = VGroup(*[
            equation.get_part_by_tex(tex, substring = False)
            for tex in self.approximation_terms
        ])
        approx_terms.set_fill(
            self.approximation_color,
            opacity = 0,
        )
        equation.add_background_rectangle()

        approx_graph = VectorizedPoint(
            self.input_to_graph_point(self.center_point, func_graph)
        )

        self.play(
            ShowCreation(func_graph, run_time = 2),
            Animation(equation),
            Animation(near_text),
        )
        for graph, term in zip(approx_graphs, approx_terms):
            self.play(
                Transform(approx_graph, graph, run_time = 2),
                Animation(equation),
                Animation(near_text),
                term.set_fill, None, 1,
            )
            self.wait()
        self.wait(2)

class ExampleApproximationWithSine(ExampleApproximation):
    CONFIG = {
        "function" : np.sin,
        "function_tex" : "\\sin(x)", 
        "order_sequence" : [1, 3, 5],
        "center_point" : 0,
        "approximation_terms" : [
            "x", 
            "-\\frac{1}{6}x^3", 
            "+\\frac{1}{120}x^5",
        ],
        "approximation_color" : GREEN,
        "x_min" : -2*np.pi,
        "x_max" : 2*np.pi,
        "x_tick_frequency" : np.pi/2,
        "y_min" : -2,
        "y_max" : 2,
        "graph_origin" : DOWN + 2*LEFT,
    }

class cos_approximation(GraphScene):

    CONFIG = {
        "x_min" : -9.5,
        "x_max" : 9.5,
        "x_tick_frequency" : 1,
        "x_axis_label": "$x$",
        "x_labeled_nums": np.arange(-8,10,2),
        "y_min" : -5,
        "y_max" : 5,
        "y_tick_frequency" : 1, 
        "y_axis_label": "$f(x)$",
        "y_labeled_nums": np.arange(-4,5,1),
        "graph_origin": ORIGIN, 
    }
    # Setup the scenes

    def setup(self):            
        GraphScene.setup(self)

    def construct(self):
        self.setup_axes(animate=True)

        #Defining own factorial function
        def factorial(n):
            fac = 1
            if n > 0:
                for i in range(1,n+1):
                    fac=fac*i
            return fac

        #Value of x using k-terms of Taylor approximation
        def taylor_approximation_cos(k,x):
            value = 0
            for i in range(k):
                value = value + ((x**(2*i)*(-1)**i)/factorial(2*i))
            return value

        #Defining the cosine function
        def cos_func(x):
            return np.cos(x) 

        cos_graph = self.get_graph(cos_func, x_min = self.x_min, x_max = self.x_max)
        cos_graph.set_color(BLUE)

        #Cosine function graph
        self.play(
            ShowCreation(cos_graph), run_time = 3
        )
        self.wait(2)


        #number of terms all bound to the top left
        term_num= [
            TextMobject("n = " + str(n))
            for n in range(0,17)
        ]
        for new_term in term_num:
            new_term.to_corner(UL)

        term = TextMobject("n = 0")
        term.to_corner(UL)
        

        #Taylor approximation of cos(x) using n-terms
        #graphing of first order outside of for loop
        graph = self.get_graph(functools.partial(taylor_approximation_cos, 0), x_min = self.x_min, x_max = self.x_max)
        self.play(ShowCreation(graph), run_time=3)
        #writing the order of terms to the top left corner
        self.play(Write(term))
        for n in range(1, 16):
            self.wait(0.5)
            new_graph = self.get_graph(functools.partial(taylor_approximation_cos, n), x_min = self.x_min, x_max = self.x_max)
            self.play(
                Transform(graph, new_graph, run_time=2),
                Transform(term, term_num[n])
            )

        self.wait()

class sin_approximation(GraphScene):

    CONFIG = {
        "x_min" : -3*np.pi,
        "x_max" : 3*np.pi,
        "x_tick_frequency" : 1,
        "x_axis_label": "$x$",
        "x_labeled_nums": np.arange(-8,8,2),
        "y_min" : -5,
        "y_max" : 5,
        "y_tick_frequency" : 1, 
        "y_axis_label": "$f(x)$",
        "y_labeled_nums": np.arange(-4,4,1),
        "graph_origin": ORIGIN, 
    }
    # Setup the scenes

    def setup(self):            
        GraphScene.setup(self)

    def construct(self):
        self.setup_axes(animate=True)

        #Defining own factorial function
        def factorial(n):
            fac = 1
            if n > 0:
                for i in range(1,n+1):
                    fac=fac*i
            return fac

        #Value of x using k-terms of Taylor approximation
        def taylor_approximation_sin(k,x):
            value = 0
            for i in range(k):
                value = value + ((x**(2*i+1)*(-1)**i)/factorial(2*i+1))
            return value

        #defining the sine function
        def sin_func(x):
            return np.sin(x) 

        sin_graph = self.get_graph(sin_func, x_min = self.x_min, x_max = self.x_max)
        sin_graph.set_color(BLUE)

        #Sine function graph
        self.play(
            ShowCreation(sin_graph), run_time = 3
        )
        self.wait(2)
        

        #number of terms all bound to the top left
        term_num= [
            TextMobject("n = " + str(n))
            for n in range(0,17)
        ]
        for new_term in term_num:
            new_term.to_corner(UL)

        term = TextMobject("n = 0")
        term.to_corner(UL)

        #Taylor approximation of sin(x) using n-terms
        #graphing of first order outside of for loop
        graph = self.get_graph(functools.partial(taylor_approximation_sin, 0), x_min = self.x_min, x_max = self.x_max)
        self.play(ShowCreation(graph), run_time=3)
        #writing the order of terms to the top left corner
        self.play(Write(term))
        for n in range(1, 16):
            self.wait(0.5)
            new_graph = self.get_graph(functools.partial(taylor_approximation_sin, n), x_min = self.x_min, x_max = self.x_max)
            self.play(
                Transform(graph, new_graph, run_time=2),
                Transform(term, term_num[n])
            )

        self.wait()

class exponential_approximation(GraphScene):

    CONFIG = {
        "x_min" : -8,
        "x_max" : 5,
        "x_tick_frequency" : 1,
        "x_axis_label": "$x$",
        #"x_labeled_nums": np.arange(-5,3,1),
        "y_min" : -1,
        "y_max" : 7,
        "y_tick_frequency" : 1, 
        "y_axis_label": "$f(x)$",
        #"y_labeled_nums": np.arange(-1,7,1),
        "graph_origin": 1*RIGHT + 2*DOWN, 
        #"graph_origin": ORIGIN, 
    }
    # Setup the scenes

    def setup(self):            
        GraphScene.setup(self)

    def construct(self):

        number_of_terms = 20
        
        self.setup_axes(animate=True)

        #Defining own factorial function
        def factorial(n):
            fac = 1
            if n > 0:
                for i in range(1,n+1):
                    fac=fac*i
            return fac

        #Value of x using k-terms of Taylor approximation
        def taylor_approximation_exp(k,x):
            value = 0
            for i in range(k):
                value = value + ((x**(i))/factorial(i))
            return value

        #defining the exp function
        def exp_func(x):
            return np.exp(x) 

        exp_graph = self.get_graph(exp_func, x_min = self.x_min, x_max = self.x_max)
        exp_graph.set_color(BLUE)

        #exp function graph
        self.play(
            ShowCreation(exp_graph), run_time = 3
        )
        self.wait(2)
        

        #number of terms all bound to the top left
        term_num= [
            TextMobject("n = " + str(n))
            for n in range(0, number_of_terms+1)
        ]
        for new_term in term_num:
            new_term.to_corner(UL)

        term = TextMobject("n = 0")
        term.to_corner(UL)

        #Taylor approximation of exp(x) using n-terms
        #graphing of first order outside of for loop
        apx_graph = self.get_graph(functools.partial(taylor_approximation_exp, 0), x_min = self.x_min, x_max = self.x_max)
        self.play(ShowCreation(apx_graph), run_time=3)
        #writing the order of terms to the top left corner
        self.play(Write(term))
        for n in range(1, number_of_terms+1):
            self.wait(0.5)
            new_graph = self.get_graph(functools.partial(taylor_approximation_exp, n), x_min = self.x_min, x_max = self.x_max)
            self.play(
                Transform(apx_graph, new_graph, run_time=1.5),
                Transform(term, term_num[n])
            )

        self.wait()