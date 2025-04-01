from manim import *
import math
import scipy as sp
import sympy

# --- Helper Function for Taylor Approximation ---
def f_deriv(f, x_val, n):
    x = sympy.symbols('x')
    f_n = f
    for _ in range(n):
        f_n = sympy.diff(f_n, x)
    return float(f_n.subs(x, x_val))

# --- Modify taylor_approx_at_a ---
def taylor_approx_at_a(f, x, a, n_terms):
    """Calculates the Taylor expansion of 1/(1+x^2) around 'a' up to n_terms.
    example Usage:
        x_sym = sympy.symbols('x')
        f_expr = math.log(x_sym)
        func = lambda x: taylor_approx_at_a(f_expr, x, 1, i)
    
    """
    val = 0.0
    a = float(a) # Ensure 'a' is a float
    x = float(x) # Ensure 'x' is a float
    for n in range(n_terms + 1):
        deriv_at_a = f_deriv(f, a, n)
        term = deriv_at_a / math.factorial(n) * (x - a)**n
        # Cap term magnitude to avoid excessive spikes when diverging
        if abs(term) > 100: # Adjust cap as needed
            term = np.sign(term) * 100
        val += term
            
    # Cap the output value
    if abs(val) > 5: # Limit based on axes range
        return np.sign(val) * 5
    return val

X_SYM = sympy.symbols('x')
COS = sympy.cos(X_SYM)
SIN = sympy.sin(X_SYM)

# FINISHED
class OpeningSzene(Scene):
    """Öffnungs Szene, in der eine Funktion, die wie eine Sinus Funktion aussieht,
    aber nicht ist, gezeigt wird. Dann wird das Bild herausgezoomt, wodurch deutlich
    wird, dass es sich nicht um eine Sinus Funktion handelt."""
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
        x_scale_factor = 2.5
        x_labels = [
            MathTex("-5\pi"),MathTex("-4\pi"),MathTex("-3\pi"), MathTex("-2\pi"), MathTex ("-\pi"), 
            MathTex("0"), 
            MathTex("\pi"), MathTex("2\pi"), MathTex("3\pi"), MathTex("4\pi"), MathTex("5\pi")
        ]
        plot = VGroup()
        for i,label in enumerate(x_labels):
            label.add_background_rectangle().next_to(np.array([ x_scale_factor*(-6 + 12/(11*np.pi) + (6-12/(11*np.pi))/5*i), 0, 0]), 0.5*DOWN).scale(0.7)
            self.add_foreground_mobject(label)
            plot = VGroup(label, plot)
        sin_graph = axes.plot(lambda x: taylor_approx_at_a(SIN, x, 0, 30), color = GREEN)
        sin_graph.apply_matrix([[x_scale_factor,0], [0,1]])
        sin_label = MathTex("f(x)=sin(x)").next_to(np.array([0.75, 1.5, 0])).set_color(GREEN)
        plot = VGroup(axes, plot)
        self.play(FadeIn(plot))
        self.play(Create(sin_graph), run_time = 5)
        self.wait()
        self.play(Write(sin_label))
        self.wait()
        self.play(
            x_labels[0].animate.shift((x_labels[0].get_x()/x_scale_factor - x_labels[0].get_x()) * RIGHT),
            x_labels[1].animate.shift((x_labels[1].get_x()/x_scale_factor - x_labels[1].get_x()) * RIGHT),
            x_labels[2].animate.shift((x_labels[2].get_x()/x_scale_factor - x_labels[2].get_x()) * RIGHT),
            x_labels[3].animate.shift((x_labels[3].get_x()/x_scale_factor - x_labels[3].get_x()) * RIGHT),
            x_labels[4].animate.shift((x_labels[4].get_x()/x_scale_factor - x_labels[4].get_x()) * RIGHT),
            x_labels[5].animate.shift((x_labels[5].get_x()/x_scale_factor - x_labels[5].get_x()) * RIGHT),
            x_labels[6].animate.shift((x_labels[6].get_x()/x_scale_factor - x_labels[6].get_x()) * RIGHT),
            x_labels[7].animate.shift((x_labels[7].get_x()/x_scale_factor - x_labels[7].get_x()) * RIGHT),
            x_labels[8].animate.shift((x_labels[8].get_x()/x_scale_factor - x_labels[8].get_x()) * RIGHT),
            x_labels[9].animate.shift((x_labels[9].get_x()/x_scale_factor - x_labels[9].get_x()) * RIGHT),
            x_labels[10].animate.shift((x_labels[10].get_x()/x_scale_factor - x_labels[10].get_x()) * RIGHT),
            ApplyMatrix([[1/x_scale_factor,0], [0,1]], sin_graph),
            run_time = 3,
        )
        self.wait()
        redbox = SurroundingRectangle(sin_label, buff = 0.1, color = RED)
        cross_1 = Line(start = redbox.get_corner(UL), end = redbox.get_corner(DR), color = RED)
        cross_2 = Line(start = redbox.get_corner(UR), end = redbox.get_corner(DL), color = RED)
        self.play(Create(redbox), GrowFromCenter(cross_1), GrowFromCenter(cross_2))
        self.wait()
        new_term = MathTex("f(x)=").next_to(sin_label.get_corner(LEFT), aligned_edge=LEFT, buff=0).set_color(GREEN)
        new_term = VGroup(new_term, MathTex("?").next_to(new_term, buff = 0.3).set_color(GREEN))
        self.play(FadeIn(new_term, shift = DOWN), FadeOut(sin_label, shift = DOWN), FadeOut(redbox, shift = DOWN), FadeOut(cross_1, shift = DOWN), FadeOut(cross_2, shift = DOWN), run_time = 2)
        self.play(FadeOut(*self.mobjects))

# FINISHED
class CosApproximationGoal(Scene):
    """Zeigt ein Beispiel für die Approximation eines Cos durch eine Taylorreihenentwicklung"""
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
            MathTex(r"-2\pi"), MathTex (r"-\pi"),
            MathTex(r""),
            MathTex(r"\pi"), MathTex(r"2\pi")
        ]
        for i, label in enumerate(x_labels):
            label.add_background_rectangle().next_to(np.array([-26/4.4+i*13/4.4, 0, 0]), DOWN).scale(0.7)
            plot = VGroup(plot, label)
        self.play(FadeIn(plot))
    
        approximation_term_parts = VGroup(MathTex("f(x) = ").set_color(GREEN).to_corner(UL), MathTex("1"), MathTex(r"-\frac{x^{2}}{2}"),
            MathTex(r"+\frac{x^{4}}{24}"), MathTex(r"-\frac{x^{6}}{720}"), MathTex(r"+\frac{x^{8}}{40320}"), MathTex(r"-\frac{x^{10}}{3628800}"),
            MathTex(r"+\frac{x^{12}}{479001600}"), MathTex(r"\cdots"))
        bgra = BackgroundRectangle(approximation_term_parts[0])
        self.play(Create(bgra))
        def show_cosine_approximation_n_to_m(start_degree, finish_degree):
            self.play(Write(approximation_term_parts[0]))
            for i in range(start_degree, finish_degree+1):
                if i == start_degree:
                    cos_appr = axes.plot(lambda x: taylor_approx_at_a(COS, x, 0, i*2), color = GREEN)
                    approximation_term_parts[i+1].scale(0.8).next_to(approximation_term_parts[i]).set_color(GREEN)
                    bgra2 = BackgroundRectangle(approximation_term_parts[:i+2])
                    self.play(Transform(bgra, bgra2), Create(cos_appr), Write(approximation_term_parts[i+1]))
                    self.wait()
                else:
                    next_iteration = axes.plot(lambda x: taylor_approx_at_a(COS, x, 0, i*2), color = GREEN)
                    if i < len(approximation_term_parts)-1:
                        approximation_term_parts[i+1].scale(0.8).next_to(approximation_term_parts[i]).set_color(GREEN)
                        bgra2 = BackgroundRectangle(approximation_term_parts[:i+2], buff=0.1)
                        self.play(Transform(bgra, bgra2), Transform(cos_appr, next_iteration), Write(approximation_term_parts[i+1]))
                    else:
                        self.play(Transform(cos_appr, next_iteration))
                    self.wait()

        show_cosine_approximation_n_to_m(0,10)
