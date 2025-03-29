"""Manim-Animiertes Video für die Taylorreihe einer Funktion"""

import math
#import functools
from manim import *
import scipy as sp
import sympy
import sys


def derivative(func, x, order=1, dx = 0.01):        #Wenn nichts anderes angegeben, wird die erste Ableitung mit dx = 0.01 zurückgegeben
    """n-te Ableitung einer Funktion an Stelle x mit dx von 0.01"""
    partial = [func(x + (i - order/2)*dx) for i in range(order+1)]
    while len(partial) > 1:
        partial = [
            (partial[j+1] - partial[j])/dx
            for j in range(len(partial)-1)
        ]
    return partial[0]

def taylor_approximation(func, term_count, center_point = 0):
    """Taylor Annäherung einer Funktion mit k Termen an Entwicklungsstelle a (bis x^term_count)"""
    coefficients = [
        derivative(func, center_point,n)/math.factorial(n)
        for n in range(term_count +1)
    ]
    return lambda x: sum([
        coefficients[n]*(x-center_point)**n
        for n in range(term_count +1)
    ])

def taylorseries_cosine(x, degree):
    """Wert von x abhängig vom Grad der Annäherung (bis x^(2*degree))"""
    return sum((-1)**i*x**(2*i)/math.factorial(2*i) for i in range(degree + 1))

def taylorseries_sine(x, degree):
    """Wert von x abhängig vom Grad der Annäherung (bis x^(2*degree+1)"""
    return sum((-1)**i*x**(2*i+1)/math.factorial(2*i+1) for i in range(degree + 1))

def taylorseries_exp(x, degree):
    """Wert von x abhängig vom Grad der Annäherung (bis x^degree)"""
    return sum(x**i/math.factorial(i) for i in range(degree + 1))

# def taylorseries_log(x, degree):
#     '''Wert von x abhängig vom Grad der Annäherung (bis x^degree), Annaeherung an Punkt 2'''
#     return math.log(2)+sum((-1)**(n+1)*(x-2)**n/(n*(2**n)) for n in range(1, degree+1))

def taylorseries_log_term(x, n, a):
        if n == 0:
            return math.log(a)
        else:
            # f^(n)(a) = (-1)^(n+1) * (n-1)! / a^n
            term_coeff = ((-1)**(n+1) * math.factorial(n-1)) / (a**n * math.factorial(n))
            return term_coeff * ((x-a)**n)

def taylorseries_log(x, max_n, a=1):
    val = 0
    try:
        # Handle x <= 0 safely for log
        if x <= 0: return -1000 # Or some large negative number outside plot range
        
        # Add f(a) term for n=0
        if max_n >= 0:
            val += math.log(a)
            
        # Add terms for n=1 to max_n
        for n in range(1, max_n + 1):
            # f^(n)(a) = (-1)^(n+1) * (n-1)! / a^n
            term_coeff = ((-1)**(n+1) * math.factorial(n-1)) / (a**n * math.factorial(n))
            val += term_coeff * ((x-a)**n)
            
        # Avoid excessively large values if the series diverges wildly outside interval
        if abs(val) > 10: return np.sign(val)*10 
        
    except (ValueError, OverflowError):
        # Handle potential math errors e.g., log(0), large factorials
        return -1000 # Indicate error or out of range
    return val

def maclaurin_approx_1_over_1px2(x, n_terms):
    val = 0.0
    for n in range(n_terms + 1):
        try:
            term = ((-1)**n) * (x**(2*n))
            # Prevent excessively large terms if x > 1
            if abs(term) > 1e6:
                 term = np.sign(term) * 1e6
            val += term
        except OverflowError:
            # If x^(2n) overflows, stop adding terms
            break
            
    # Cap the output value to prevent extreme spikes when diverging
    if abs(val) > 5: # Limit based on typical axes range
         return np.sign(val) * 5
    # Return NaN outside [-1, 1] to visually show divergence sharply? No, let plot range handle it.
    return val

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
        sin_graph = axes.plot(lambda x: taylorseries_sine(x,15), color = GREEN)
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
                    cos_appr = axes.plot(lambda x: taylorseries_cosine(x, i), color = GREEN)
                    approximation_term_parts[i+1].scale(0.8).next_to(approximation_term_parts[i]).set_color(GREEN)
                    bgra2 = BackgroundRectangle(approximation_term_parts[:i+2])
                    self.play(Transform(bgra, bgra2), Create(cos_appr), Write(approximation_term_parts[i+1]))
                    self.wait()
                else:
                    next_iteration = axes.plot(lambda x: taylorseries_cosine(x, i), color = GREEN)
                    if i < len(approximation_term_parts)-1:
                        approximation_term_parts[i+1].scale(0.8).next_to(approximation_term_parts[i]).set_color(GREEN)
                        bgra2 = BackgroundRectangle(approximation_term_parts[:i+2], buff=0.1)
                        self.play(Transform(bgra, bgra2), Transform(cos_appr, next_iteration), Write(approximation_term_parts[i+1]))
                    else:
                        self.play(Transform(cos_appr, next_iteration))
                    self.wait()

        show_cosine_approximation_n_to_m(0,10)

# FINISHED
class CosApproximationTut(ZoomedScene):
    """Erklärt die Berechnung der Approximation eines Cos durch eine
    Taylorreihenentwicklung zuerst visuell und dann mathematisch"""
    def __init__(self, **kwargs):
        ZoomedScene.__init__(
            self,
            zoom_factor=0.3,
            zoomed_display_height=3,
            zoomed_display_width=8,
            image_frame_stroke_width=1,
            zoomed_camera_config={
                "default_frame_stroke_width": 1,
                },
            **kwargs
        )

    def construct(self):
        apprx_color = PURPLE_C
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
        for i,label in enumerate(x_labels):
            label.add_background_rectangle().next_to(np.array([-26/4.4+i*13/4.4, 0, 0]), DOWN).scale(0.7)
            plot = VGroup(plot,label)
        cos_graph = axes.plot(lambda x: math.cos(x) , color = GREEN)
        self.play(FadeIn(VGroup(axes, plot).shift(0.5*DOWN)))
        self.wait()
        self.play(Create(cos_graph.shift(0.5*DOWN)))
        self.wait()
        cos_label = MathTex("f(x)=cos(x)").set_color(GREEN).to_corner(UL).scale(0.8)
        self.play(Write(cos_label))
        graphstuff = VGroup(plot, cos_graph, cos_label)
        self.wait()
        self.play(FadeOut(graphstuff))
        self.wait()

        ###### VISUAL WAY
        def first_order():
            title = Tex("Visual Way").scale(3)
            self.play(Write(title))
            self.wait()
            self.play(AnimationGroup(FadeOut(title), FadeIn(graphstuff), lag_ratio=0.3))
            global constant
            global apprx_func
            global constant_rectangle
            global apprx_term
            apprx_term = MathTex("a(x)=").scale(0.8).to_corner(UR).shift(4.2*LEFT).set_color(apprx_color)
            c_1 = ValueTracker(0)
            constant = always_redraw(
                lambda:
                    DecimalNumber(include_sign=True).set_value(c_1.get_value()).next_to(apprx_term.get_corner(RIGHT), aligned_edge= LEFT, buff = 0.1).scale(0.8).set_color(apprx_color)
            )
            constant_rectangle = SurroundingRectangle(constant, buff = 0.1, color = ORANGE)
            apprx_func = always_redraw(
                lambda:
                    axes.plot(
                        lambda x:
                        c_1.get_value()).set_color(apprx_color)
                )
            self.play(Write(VGroup(apprx_term, constant, constant_rectangle)))
            self.play(Create(apprx_func))
            self.wait()
            self.play(c_1.animate.set_value(-2), run_time = 2)
            self.wait()
            self.play(c_1.animate.set_value(1), run_time =2)
            self.wait()

        def second_order():
            global constant_2
            global apprx_func_2
            global stuff_2
            c_2 = ValueTracker(0)
            constant_2 = always_redraw(
                lambda:
                    DecimalNumber(include_sign=True).set_value(c_2.get_value()).next_to(constant.get_corner(RIGHT), aligned_edge= LEFT, buff = 0.1).scale(0.8).set_color(apprx_color)
            )
            constant_rectangle_temp = SurroundingRectangle(constant_2, buff = 0.1, color = ORANGE)
            stuff_2 = MathTex(r"\cdot{x}").scale(0.7).next_to(constant_2.get_corner(RIGHT), aligned_edge = LEFT, buff = 0.15).set_color(apprx_color)
            apprx_func_2 = always_redraw(
                lambda:
                    axes.plot(
                        lambda x:
                        c_2.get_value()*x+1).set_color(apprx_color)
                )
            self.play(Write(VGroup(constant_2, stuff_2)))
            self.play(Transform(constant_rectangle, constant_rectangle_temp))
            self.remove(apprx_func)
            self.add(apprx_func_2)
            self.wait()
            self.play(c_2.animate.set_value(-0.5), run_time = 2)
            self.wait()
            self.play(c_2.animate.set_value(0.5), run_time =2)
            self.wait()
            self.play(c_2.animate.set_value(0), run_time =2)
            self.wait()

        def third_order():
            global constant_3
            global apprx_func_3
            global stuff_3
            c_3 = ValueTracker(0)
            constant_3 = always_redraw(
                lambda:
                    DecimalNumber(include_sign=True).set_value(c_3.get_value()).next_to(stuff_2.get_corner(RIGHT), aligned_edge= LEFT, buff = 0.1).scale(0.8).set_color(apprx_color)
            )
            constant_rectangle_temp = SurroundingRectangle(constant_3, buff = 0.1, color = ORANGE)
            stuff_3 = MathTex(r"\cdot{x}^{2}").scale(0.7).next_to(constant_3.get_corner(RIGHT), aligned_edge = LEFT, buff = 0.15).set_color(apprx_color).shift(0.05*UP)
            apprx_func_3 = always_redraw(
                lambda:
                    axes.plot(
                        lambda x:
                        c_3.get_value()*x**2+1).set_color(apprx_color)
                )
            self.play(Write(VGroup(constant_3, stuff_3)))
            self.play(Transform(constant_rectangle, constant_rectangle_temp))
            self.remove(apprx_func_2)
            self.add(apprx_func_3)
            self.wait()
            zoomed_camera = self.zoomed_camera
            zoomed_display = self.zoomed_display
            frame = zoomed_camera.frame
            zoomed_display_frame = zoomed_display.display_frame

            frame.move_to(0.7*UP)
            frame.set_color(LIGHT_BROWN)
            zoomed_display_frame.set_color(RED)
            zoomed_display.move_to(0.7*UP)

            zd_rect = BackgroundRectangle(zoomed_display, fill_opacity=0, buff=MED_SMALL_BUFF)
            self.add_foreground_mobject(zd_rect)

            unfold_camera = UpdateFromFunc(zd_rect, lambda rect: rect.replace(zoomed_display))

            self.play(Create(frame))
            self.activate_zooming()

            self.play(self.get_zoomed_display_pop_out_animation(), unfold_camera)
            self.wait()
            self.play(c_3.animate.set_value(-1), run_time = 2)
            self.wait()
            self.play(c_3.animate.set_value(1), run_time = 4)
            self.wait()
            self.play(c_3.animate.set_value(-0.5), run_time =3)
            formula_tr = VGroup(constant, constant_2, constant_3, stuff_2, stuff_3, constant_rectangle, apprx_term)
            graphstuff_1 = VGroup(graphstuff, apprx_func_3)
            self.wait()
            self.play(self.get_zoomed_display_pop_out_animation(), unfold_camera, rate_func=lambda t: smooth(1 - t))
            self.play(Uncreate(zoomed_display_frame), FadeOut(frame))
            self.wait()
            self.play(FadeOut(formula_tr), FadeOut(graphstuff_1))
            self.wait()

        ###### CALCULATED WAY
        def first_order_calc():
            global approximation_graph
            title = Tex("Calculated Way").scale(3)
            self.play(Write(title))
            self.wait()
            self.play(AnimationGroup(FadeOut(title), FadeIn(graphstuff)))
            global approximation
            global approximation_graph
            approximation = MathTex("a(x) = a_{0}").scale(0.8).to_corner(UR).shift(4.2*LEFT).set_color(apprx_color)
            self.play(Write(approximation))
            self.wait()
            # cos Punkt bei x = 0 und Pfeil der darauf zeigt
            point_1 = Dot(point=axes.coords_to_point(0,1,0))
            pointer_1 = Arrow(start = axes.coords_to_point(1,1.25,0), end = axes.coords_to_point(0.1, 1.025,0), buff = 0, color = WHITE)
            self.play(FadeIn(pointer_1), FadeIn(point_1))
            self.wait()
            self.play(Transform(approximation, MathTex("a(0) = f(0)").scale(0.8).next_to(approximation, direction = 0, aligned_edge=LEFT, buff =0).set_color(apprx_color)))
            self.wait()
            approximation_side_calc = MathTex("= cos(0)").scale(0.8).next_to(approximation[0][4], direction = DOWN, aligned_edge=LEFT).set_color(apprx_color)
            approximation_side_calc_2 = MathTex("= 1").scale(0.8).next_to(approximation_side_calc, direction = DOWN, aligned_edge=LEFT).set_color(apprx_color)
            approximation_graph = axes.plot(lambda x: 1, color = apprx_color)
            self.play(FadeIn(approximation_side_calc, shift = DOWN))
            self.wait()
            self.play(FadeIn(approximation_side_calc_2, shift = DOWN))
            self.wait()
            self.play(FadeOut(approximation_side_calc), FadeOut(approximation_side_calc_2[0][0]) ,FadeOut(approximation[0][5:]),approximation_side_calc_2.animate.shift((approximation.get_y() - approximation_side_calc_2.get_y())*UP))
            approximation = VGroup(approximation[0][:5], approximation_side_calc_2[0][1:])
            self.wait()
            self.play(FadeOut(point_1), FadeOut(pointer_1))
            self.play(Create(approximation_graph))
            self.wait()

        def second_order_calc():
            global cos_fd
            cos_fd = MathTex("f'(x) = sin(x)").next_to(cos_label, direction=DOWN).to_edge(LEFT).scale(0.8).set_color(GREEN)
            self.play(ReplacementTransform(cos_label.copy(), cos_fd))
            self.wait()
            second_order_coeff = MathTex("+ a_{1}x").scale(0.8).next_to(approximation, direction = RIGHT, buff = 0).shift(0.07*RIGHT + 0.04*DOWN).set_color(apprx_color)
            self.play(Transform(approximation[0][2], MathTex("x").scale(0.8).next_to(approximation[0][2], aligned_edge=LEFT, buff = 0).shift(0.1*LEFT+0.05*DOWN).set_color(apprx_color)), Write(second_order_coeff))
            self.wait()
            approximation_side_calc = MathTex("a'(x) = a_{1}").scale(0.8).next_to(approximation, direction=DOWN, aligned_edge=LEFT).set_color(apprx_color)
            approximation_side_calc2 = MathTex("a'(0) = a_{1}").scale(0.8).next_to(approximation_side_calc, direction=DOWN, aligned_edge=LEFT).set_color(apprx_color)
            approximation_side_calc3 = MathTex("a'(0) = f'(0)").scale(0.8).next_to(approximation_side_calc2, direction=DOWN, aligned_edge=LEFT).set_color(apprx_color)
            approximation_side_calc3[0][6:].set_color(GREEN)
            approximation_side_calc4 = MathTex("a_{1} = f'(0)").scale(0.8).next_to(approximation_side_calc3).set_color(apprx_color).shift((approximation_side_calc2.get_y() - approximation_side_calc3.get_y())/2*UP + RIGHT)
            arrow_1 = Arrow(start = approximation_side_calc2.get_corner(RIGHT) + (0.47,0,0), end = approximation_side_calc4.get_corner(LEFT) + (0,0.1,0), buff = 0.2, stroke_width=2)
            arrow_2 = Arrow(start = approximation_side_calc3.get_corner(RIGHT), end = approximation_side_calc4.get_corner(LEFT) + (0,-0.1,0), buff = 0.2, stroke_width=2)
            self.wait()
            self.play(FadeIn(approximation_side_calc, shift = DOWN))
            self.wait()
            self.play(FadeIn(approximation_side_calc2, shift = DOWN))
            self.wait()
            self.play(FadeIn(approximation_side_calc3, shift = DOWN))
            self.wait()
            self.play(Write(arrow_1), Write(arrow_2))
            self.wait()
            self.play(Write(approximation_side_calc4))
            self.wait()
            rect_1 = SurroundingRectangle(approximation_side_calc4[0][3:])
            rect_2 = SurroundingRectangle(cos_fd)
            self.play(Create(rect_1), Create(rect_2))
            self.wait()
            self.play(Uncreate(rect_1), Uncreate(rect_2))
            self.wait()
            self.play(Transform(approximation_side_calc4[0][3:], MathTex("sin(0)").scale(0.8).set_color(apprx_color).next_to(approximation_side_calc4[0][3], aligned_edge=LEFT,direction=0,buff =0)))
            self.wait()
            self.play(Transform(approximation_side_calc4[0][3:], MathTex("0").scale(0.8).set_color(apprx_color).next_to(approximation_side_calc4[0][3], aligned_edge=LEFT,direction=0,buff =0)))
            self.wait()
            self.play(FadeOut(approximation_side_calc), FadeOut(approximation_side_calc2), FadeOut(approximation_side_calc3), FadeOut(approximation_side_calc4), FadeOut(arrow_1), FadeOut(arrow_2), Transform(second_order_coeff[0][1:], MathTex("0 x").scale(0.8).set_color(apprx_color).next_to(second_order_coeff[0][1], aligned_edge=LEFT, direction=0, buff=0)))
            self.wait()
            cross_out_line = Line(start = second_order_coeff.get_corner(DL), end = second_order_coeff.get_corner(UR), color = RED)
            self.play(Create(cross_out_line))
            self.wait()
            self.play(FadeOut(second_order_coeff), FadeOut(cross_out_line))
            self.wait()

        def third_order_calc():
            global approximation_side_calc_4
            global third_term_coeff
            global cos_sd
            cos_sd = MathTex("f''(x) = -cos(x)").next_to(cos_fd, direction=DOWN).to_edge(LEFT).scale(0.8).set_color(GREEN)
            self.play(ReplacementTransform(cos_fd.copy(), cos_sd))
            self.wait()
            third_term_coeff = MathTex(r"+a_{2}x^{2}").scale(0.8).next_to(approximation, direction=RIGHT, buff=0).shift(0.07*RIGHT+0.02*UP).set_color(apprx_color)
            self.play(Write(third_term_coeff))
            self.wait()
            approximation_side_calc = MathTex("a'(x) = a_{2} \cdot 2x").scale(0.8).next_to(approximation, direction = DOWN, aligned_edge = LEFT).set_color(apprx_color)
            approximation_side_calc_2 = MathTex("a''(x) = a_{2} \cdot 2").scale(0.8).next_to(approximation_side_calc, direction = DOWN, aligned_edge = LEFT).set_color(apprx_color)
            approximation_side_calc_3 = MathTex("a''(0) = f''(0)").scale(0.8).next_to(approximation_side_calc_2, direction=DOWN, aligned_edge=LEFT).set_color(apprx_color)
            approximation_side_calc_3[0][7:].set_color(GREEN)
            approximation_side_calc_4 = MathTex("2 \cdot a_{2} = f''(0)").scale(0.8).next_to(approximation_side_calc_3).shift((approximation_side_calc_2.get_y()-approximation_side_calc_3.get_y())/2 * UP + 0.9*RIGHT).set_color(apprx_color)
            approximation_side_calc_4[0][5:].set_color(GREEN)
            arrow_1 = Arrow(start = approximation_side_calc_2.get_corner(RIGHT), end = approximation_side_calc_4.get_corner(LEFT) + (0,0.1,0), buff = 0.2, stroke_width=2)
            arrow_2 = Arrow(start = approximation_side_calc_3.get_corner(RIGHT), end = approximation_side_calc_4.get_corner(LEFT) + (0,-0.1,0), buff = 0.2, stroke_width=2)
            self.play(FadeIn(approximation_side_calc, shift = DOWN))
            self.wait()
            self.play(FadeIn(approximation_side_calc_2, shift = DOWN))
            self.wait()
            self.play(FadeIn(approximation_side_calc_3, shift = DOWN))
            self.wait()
            self.play(Write(arrow_1), Write(arrow_2))
            self.wait()
            self.play(Write(approximation_side_calc_4))
            self.wait()
            rect_1 = SurroundingRectangle(approximation_side_calc_4[0][5:])
            rect_2 = SurroundingRectangle(cos_sd)
            self.play(Create(rect_1), Create(rect_2))
            self.wait()
            self.play(Uncreate(rect_1), Uncreate(rect_2))
            self.wait()
            self.play(Transform(approximation_side_calc_4[0][5:], MathTex("-cos(0)").scale(0.8).set_color(GREEN).next_to(approximation_side_calc_4[0][5], aligned_edge=LEFT, buff = -0.1)))
            self.wait()
            self.play(Transform(approximation_side_calc_4[0][5:], MathTex("-1").scale(0.8).set_color(GREEN).next_to(approximation_side_calc_4[0][5][0], aligned_edge=LEFT, buff = -0.1).shift(0.02*UP)))
            self.wait()
            right_side = MathTex(r"\frac{1}{2}").scale(0.7).move_to(approximation_side_calc_4[0][-1]).shift(0.2*RIGHT)
            right_side[0][0].set_color(apprx_color)
            right_side[0][2].set_color(GREEN)
            self.play(AnimationGroup(
                        FadeOut(approximation_side_calc_4[0][0:2]),
                        #Transform(approximation_side_calc_4[0][2:], approximation_side_calc_4[0][2:].shift(0.5*LEFT)),
                        Transform(approximation_side_calc_4[0][5][1:], right_side),
                        lag_ratio=0.3))
            self.wait()
            self.play(FadeOut(VGroup(approximation_side_calc[0], approximation_side_calc_2, approximation_side_calc_3, approximation_side_calc_4[0][2:5], arrow_1, arrow_2, third_term_coeff[0][:3])), approximation_side_calc_4[0][5][0:].animate.shift((third_term_coeff[0][0].get_y()-approximation_side_calc_4[0][5][0].get_y())*UP + (third_term_coeff[0][0].get_x()-approximation_side_calc_4[0][5][0].get_x())*RIGHT))
            self.play(approximation_side_calc_4[0][5][0:].animate.set_color(apprx_color))
            self.wait()
            self.play(Transform(approximation_graph, axes.plot(lambda x: 1-x**2/2).set_color(apprx_color)))
            self.wait()
        
        def show_more_terms():
            self.wait()
            function_term = VGroup(approximation, third_term_coeff[0][3:],approximation_side_calc_4[0][5])
            function_term.shift(3*LEFT)

            new_term = MathTex(r'+\frac{x^4}{24}').scale(0.8).set_color(apprx_color).next_to(approximation_side_calc_4[0][5], direction=RIGHT, buff = 0.6)
            function_term.add(new_term)
            self.play(Transform(approximation_graph, axes.plot(lambda x: taylorseries_cosine(x,2)).set_color(apprx_color)),
                        Write(new_term))
            self.wait()

            new_term = MathTex(r'-\frac{x^6}{720}').scale(0.8).set_color(apprx_color).next_to(new_term, direction=RIGHT, buff = 0.1)
            function_term.add(new_term)
            self.play(Transform(approximation_graph, axes.plot(lambda x: taylorseries_cosine(x,3)).set_color(apprx_color)),
                        Write(new_term))
            self.wait()

            new_term = MathTex(r'+\frac{x^8}{40320}').scale(0.8).set_color(apprx_color).next_to(new_term, direction=RIGHT, buff = 0.1)
            function_term.add(new_term)
            self.play(Transform(approximation_graph, axes.plot(lambda x: taylorseries_cosine(x,4)).set_color(apprx_color)),
                        Write(new_term))
            self.wait()

            new_term = MathTex(r'-\frac{x^{10}}{3628800}').scale(0.8).set_color(apprx_color).next_to(new_term, direction=RIGHT, buff = 0.1)
            function_term.add(new_term)
            self.play(Transform(approximation_graph, axes.plot(lambda x: taylorseries_cosine(x,5)).set_color(apprx_color)),
                        Write(new_term))
            self.wait()
            #self.play(FadeOut(function_term))

        first_order()
        second_order()
        third_order()

        first_order_calc()
        second_order_calc()
        third_order_calc()
        show_more_terms()

# ROADMAP MAYBE NOT FINISHED
class full_formula(Scene):
    def construct(self):
        apprx_color = PURPLE_C
        axes = Axes(
            x_range = [-10, 10, 2],
            y_range = [-6, 6],
            x_length = 13,
            y_length = 7,
            axis_config={"color": BLUE, "include_numbers": True, "decimal_number_config": {"num_decimal_places": 0}},
            #y_axis_config={"include_numbers": True, "decimal_number_config": {"num_decimal_places": 0}},
            tips = True
        )

        def roadmap_text_and_formula():
            '''Writes the roadmap of how to get the full formula to the left of the screen'''
            step_1 = Text("1: Werte der n-ten Ableitung des Polynom\nund der zu approximierenden Funktion\nsollen an der Entwicklungsstelle\nidentisch sein").scale(0.61).to_corner(UL).shift(0.5*DOWN)
            step_2 = Text("2: Polynomreihe mit unendlich vielen\nTermen für die höchste Genauigkeit").scale(0.61).next_to(step_1, direction=DOWN, aligned_edge=LEFT, buff = 0.4)
            step_3 = Text("3: Der n-te Term der Reihe repräsentiert\ndie Ableitungsinformation der n-ten\nAbleitung der zu approximierenden Funktion").scale(0.61).next_to(step_2, direction=DOWN, aligned_edge=LEFT, buff = 0.4)

            #formula 1 to top right
            formula_1 = MathTex(r"T_{n}\left(x\right)=\frac{c\cdot x^{n}}{n!}").scale(0.8).to_corner(UR).shift(0.5*DOWN+1*LEFT)
            formula_2 = MathTex(r"T_{n}^{\left(n\right)}\left(x\right)=\frac{c\cdot n!}{n!}").scale(0.8).next_to(formula_1, direction=DOWN, aligned_edge=LEFT, buff = 0.5)
            
            # formula 3 in the lower center
            formula_3_1 = MathTex(r"T(x)=?").scale(0.9).to_edge(DOWN).shift(0.5*UP)
            formula_3_2 = MathTex(r"T\left(x\right)=\sum_{n=0}^{\infty}\frac{f^{\left(n\right)}\left(0\right)}{n!}\cdot x^{n}").scale(0.9).to_edge(DOWN).shift(0.5*UP)

            self.play(Write(step_1))
            self.wait()
            self.play(Write(step_2))
            self.wait()
            self.play(Write(step_3))
            self.wait()

            self.play(Write(formula_3_1))
            self.wait()
            self.play(Write(formula_1))
            self.wait()
            self.play(Write(formula_2))
            self.wait()

            # cancel out the n!/n! in the second formula
            self.play(formula_2[0][11:13].animate.set_color(RED), formula_2[0][14:16].animate.set_color(RED))
            self.wait()
            self.play(FadeOut(formula_2[0][10:]), formula_2[0][9].animate.shift(0.27*DOWN))
            self.wait()

            # draw a box around the second bullet point
            redbox = SurroundingRectangle(step_2, color=RED)
            self.play(Create(redbox))

            #replace c with f^(n)(0)
            self.play(Transform(formula_2[0][9], MathTex(r"f^{\left(n\right)}\left(0\right)").scale(0.8).next_to(formula_2[0][9], aligned_edge=LEFT, buff = 0)))
            self.wait()

            # remove the redbox
            self.play(FadeOut(redbox))

            def apply_function(mob):
                mob.stretch_to_fit_width(2.2)
                mob.shift(0.65*RIGHT)
                return mob
            
            self.play(
                    # replace c at the top formula with f^(n)(0)
                    Transform(formula_1[0][6], MathTex(r"f^{\left(n\right)}\left(0\right)").scale(0.75).next_to(formula_1[0][6], aligned_edge=LEFT, buff = 0).shift(0.05*UP)),
                    
                    # shift *x^n to the right of the replaced c
                    formula_1[0][7:10].animate.shift(1.05*RIGHT),
                    
                    # make the fractions line bigger in the x direction
                    ApplyFunction(apply_function, formula_1[0][10]),

                    # move the denominator of the fraction to the right
                    formula_1[0][11:].animate.shift(0.65*RIGHT),
            )


            # show final formula
            self.play(Transform(formula_3_1, formula_3_2))
            self.wait()

            # can we just just a instead of 0?
            self.play(Transform(formula_3_1[0][15], MathTex(r"a").scale(0.9).next_to(formula_3_1[0][15].get_corner(LEFT), aligned_edge=LEFT, buff = 0)))
            self.wait()

            # Fade out everything except formula_3_1. Move it to the top left
            self.play(FadeOut(VGroup(step_1, step_2, step_3, formula_1, formula_2[0][:10])))

            def move_to_top_left(mob):
                mob.to_corner(UL)
                mob[0][0:4].set_color(GOLD_C)
                return mob
            self.play(ApplyFunction(move_to_top_left, formula_3_1))
            self.wait()

            # add the axes and plot a formula
            axes_labels = axes.get_axis_labels()
            self.play(Create(axes), Write(axes_labels))
            self.wait()
            def func(x):
                return math.cos(x)-0.1*x**2+0.003*x**3+0.3*x+4+0.0004*x**4
            plt = axes.plot(lambda x: func(x), color=BLUE)
            self.play(Write(plt))
            self.wait()

            # add dashed line at x = 2
            dashed_line = DashedLine(start=axes.coords_to_point(2,-10), end=axes.coords_to_point(2,10), color=RED)
            self.play(Create(dashed_line))
            self.wait()

            # transform a in formula_3_1 to 2
            self.play(Transform(formula_3_1[0][15], MathTex(r"2").scale(0.9).next_to(formula_3_1[0][15].get_corner(LEFT), aligned_edge=LEFT, buff = 0)))
            self.wait()

            # ValueTracker for parameter 'a'
            a_tracker = ValueTracker(0)

            # Define the graph with respect to 'a'
            graph = always_redraw(lambda: axes.plot(
                lambda x: func(x + a_tracker.get_value() + 2), color=GOLD_C
            ))

            # Dashed line
            def get_dashed_line():
                start_point = axes.c2p(2, func(2))
                end_point = axes.c2p(-a_tracker.get_value(), func(2))
                return DashedLine(start_point, end_point, dash_length=0.1).set_color(YELLOW)
            
            dashed_line_hor = always_redraw(get_dashed_line)

            self.play(Write(graph))
            self.wait()
            self.play(Create(dashed_line_hor))
            self.wait()

            # move x a litle bit to the right, insert a ( before it, add the value tracker a after it, and add a ) after it, move the ^n behind the )
            constant_a = always_redraw(
                lambda:
                    DecimalNumber(include_sign=True).set_value(a_tracker.get_value()).next_to(formula_3_1[0][21].get_corner(RIGHT), aligned_edge= LEFT, buff = 0.1).scale(0.9)
            )
            constant_a_rectangle = SurroundingRectangle(constant_a, buff = 0.1, color = GREEN_B)

            # Add background rectangle for the formule. Shift as workaround
            self.add(VGroup(formula_3_1, constant_a, constant_a_rectangle.shift(0.6*RIGHT)).add_background_rectangle())
            constant_a_rectangle.shift(0.5*LEFT)
            
            parenthesis_left = MathTex(r"(").scale(0.9).next_to(formula_3_1[0][20].get_corner(RIGHT), aligned_edge=LEFT, buff = 0.1)
            parenthesis_right = MathTex(r")").scale(0.9).next_to(formula_3_1[0][21].get_corner(RIGHT), aligned_edge=LEFT, buff = 1.45)

            self.play(
                formula_3_1[0][21].animate.shift(0.1*RIGHT),
                formula_3_1[0][22].animate.shift(1.55*RIGHT),
                FadeIn(parenthesis_left),
                FadeIn(parenthesis_right),
                FadeIn(constant_a_rectangle),
                FadeIn(constant_a.shift(0.1*RIGHT)),
            )

            self.wait()
    
            self.play(a_tracker.animate.set_value(2), run_time=3)
            self.wait()
            self.play(a_tracker.animate.set_value(-2), run_time=3)
            self.wait()

            # Fade out everything except formula_3_1. Move it back to the center
            self.play(FadeOut(VGroup(axes, graph, dashed_line_hor, dashed_line, constant_a_rectangle, plt, axes_labels)))
            def move_to_center(mob):
                mob.move_to(ORIGIN)
                mob.set_color(WHITE)
                return mob
            # vgroup everything thats on the screen
            self.play(ApplyFunction(move_to_center, VGroup(formula_3_1, parenthesis_left, parenthesis_right)))

            self.wait()

            # replace the fixed values 2 with approximation point a
            self.play(Transform(formula_3_1[0][15], MathTex(r"a").scale(0.9).next_to(formula_3_1[0][15].get_corner(LEFT), aligned_edge=LEFT, buff = 0).shift(0.05*DOWN)),
                      Transform(constant_a, MathTex(r"- a").scale(0.9).next_to(formula_3_1[0][21].get_corner(RIGHT), aligned_edge=LEFT, buff = 0.1)),
                      parenthesis_right.animate.shift(0.6*LEFT),
                      formula_3_1[0][22].animate.shift(0.6*LEFT),
            )

            # Move formula to the top for the Cos_Formula_Deviation Scene
            formula_3_1.to_corner(UL)

        roadmap_text_and_formula()

# FINISHED
class Cos_Formula_Deviation(Scene):
    def construct(self):
        # Write taylore formula
        taylor_formula = MathTex(r"T(x)=\sum_{n=0}^{\infty}\frac{f^{\left(n\right)}\left(0\right)}{n!}\cdot x^{n}").scale(0.9).to_edge(UP).shift(0.5*DOWN)
        self.play(Write(taylor_formula))
        self.wait()

        # Mark the n-th derivative to show that this is the only part that depends on the function we approximate
        ###################################
        ########################
        ##############

        # Can we find a general formula for the nth derivative of cos(x)?
        gap = 0.5
        cos_func = MathTex("f(x)=cos(x)").to_corner(UL).scale(0.8).shift(0.3*RIGHT)
        self.play(Write(cos_func))
        self.wait()
        cos_fd = MathTex("f'(x)=-sin(x)").scale(0.8).next_to(cos_func.get_corner(LEFT), direction=DOWN, aligned_edge=LEFT, buff = gap)
        self.play(Write(cos_fd))
        self.wait()
        cos_sd = MathTex("f''(x)=-cos(x)").scale(0.8).next_to(cos_fd.get_corner(LEFT), direction=DOWN, aligned_edge=LEFT, buff = gap)
        self.play(Write(cos_sd))
        self.wait()
        cos_td = MathTex("f'''(x)=sin(x)").scale(0.8).next_to(cos_sd.get_corner(LEFT), direction=DOWN, aligned_edge=LEFT, buff = gap)
        self.play(Write(cos_td))
        self.wait()
        cos_fod = MathTex("f^{(4)}(x)=cos(x)").scale(0.8).next_to(cos_td.get_corner(LEFT), direction=DOWN, aligned_edge=LEFT, buff = gap)
        self.play(Write(cos_fod))
        self.wait()

        # show that we are again at cos and the cycle repeats
        self.play(cos_func[0][5:].animate.set_color(RED),
                  cos_fod[0][8:].animate.set_color(RED))
        self.wait()

        # add a "recycle" arrow from fod to func with an equivalent symbol
        recycle_arrow = CurvedArrow(start_point=cos_fod.get_corner(DL)+0.2*DOWN, end_point=cos_func.get_corner(UL)+0.2*UP, color=RED, radius=-3).scale(0.8)
        equivalent_symbol = MathTex(r"\Leftrightarrow").set_color(RED).scale(0.8).next_to(recycle_arrow, direction=RIGHT, buff = -0.75).add_background_rectangle()
        self.play(Write(recycle_arrow), Write(equivalent_symbol))
        self.wait()
        
        # Move taylor function to the right
        self.play(taylor_formula.animate.shift(3*RIGHT))
        self.wait()

        # We want to approxiamte cos(x) at x = 0. Lets see what the derivative values are at x = 0
        # 1. replace all x with 0
        buff_2 = -0.09
        self.play(Transform(cos_func[0][2], MathTex(r"0").scale(0.8).next_to(cos_func[0][2], aligned_edge=LEFT, buff = buff_2)),
                Transform(cos_func[0][9], MathTex(r"0").set_color(RED).scale(0.9).next_to(cos_func[0][9], aligned_edge=LEFT, buff = buff_2)),
                Transform(cos_fd[0][3], MathTex(r"0").scale(0.8).next_to(cos_fd[0][3], aligned_edge=LEFT, buff = buff_2)),
                Transform(cos_fd[0][11], MathTex(r"0").scale(0.9).next_to(cos_fd[0][11], aligned_edge=LEFT, buff = buff_2)),
                Transform(cos_sd[0][4], MathTex(r"0").scale(0.8).next_to(cos_sd[0][4], aligned_edge=LEFT, buff = buff_2)),
                Transform(cos_sd[0][12], MathTex(r"0").scale(0.9).next_to(cos_sd[0][12], aligned_edge=LEFT, buff = buff_2)),
                Transform(cos_td[0][5], MathTex(r"0").scale(0.8).next_to(cos_td[0][5], aligned_edge=LEFT, buff = buff_2)),
                Transform(cos_td[0][12], MathTex(r"0").scale(0.9).next_to(cos_td[0][12], aligned_edge=LEFT, buff = buff_2)),
                Transform(cos_fod[0][5], MathTex(r"0").scale(0.8).next_to(cos_fod[0][5], aligned_edge=LEFT, buff = buff_2)),
                Transform(cos_fod[0][12], MathTex(r"0").set_color(RED).scale(0.9).next_to(cos_fod[0][12], aligned_edge=LEFT, buff = buff_2)),
                )
        self.wait()
        
        # 2. add the = sign and the corresponding values
        values = [MathTex(r"=1"), MathTex(r"=0"), MathTex(r"=-1"), MathTex(r"=0"), MathTex(r"=1"), MathTex(r"=0"), MathTex(r"=-1"), MathTex(r"=0")]
        buff_3 = 0.2
        self.play(AnimationGroup(
            Write(values[0].scale(0.9).next_to(cos_func, direction=RIGHT, buff = buff_3)),
            Write(values[1].scale(0.9).next_to(cos_fd, direction=RIGHT, buff = buff_3)),
            Write(values[2].scale(0.9).next_to(cos_sd, buff = buff_3)),
            Write(values[3].scale(0.9).next_to(cos_td, buff = buff_3)),
            Write(values[4].scale(0.9).next_to(cos_fod, buff = buff_3)),
            lag_ratio=0.3
        ))
        self.wait()
        def v1():
            # 3.2.1 Write down what plugging these derivate values would look like in the series
            series_aprx = MathTex(r"T(x)=\frac{1}{0!}\cdot x^{0}+\frac{0}{1!}\cdot x^{1}+\frac{-1}{2!}\cdot x^{2}+\frac{0}{3!}\cdot x^{3}+\frac{1}{4!}\cdot x^{4}+\frac{0}{5!}\cdot x^{5}+\frac{-1}{6!}\cdot x^{6}+\frac{0}{7!}\cdot x^{7}+\cdots").scale(0.7).to_edge(DOWN).shift(0.5*UP)
            self.play(Write(series_aprx))
            self.wait()

            # 3.2.2 Show where these values come from. read formula and mark the coefficients in the top left
            # mark coefficient in top left
            rect_f = SurroundingRectangle(cos_func, color=GREEN_B, buff=0.15).stretch_to_fit_width(4.5).shift(RIGHT)
            rect_t = SurroundingRectangle(series_aprx[0][5:12], color=GREEN_B, buff=0.075)

            self.play(Create(rect_f), Create(rect_t), series_aprx[0][5].animate.set_color(YELLOW), values[0][0][1:].animate.set_color(YELLOW))
            self.wait()
            # move the rectangles to the next coefficient
            self.play(rect_f.animate.shift(0.72*DOWN), rect_t.animate.shift(1.45*RIGHT).stretch_to_fit_width(1.22), series_aprx[0][5].animate.set_color(WHITE), values[0][0][1:].animate.set_color(WHITE),series_aprx[0][13].animate.set_color(YELLOW), values[1][0][1:].animate.set_color(YELLOW))
            self.wait()
            self.play(rect_f.animate.shift(0.72*DOWN), rect_t.animate.shift(1.45*RIGHT), series_aprx[0][13].animate.set_color(WHITE), values[1][0][1:].animate.set_color(WHITE),series_aprx[0][21:23].animate.set_color(YELLOW), values[2][0][1:].animate.set_color(YELLOW))
            self.wait()
            self.play(rect_f.animate.shift(0.72*DOWN), rect_t.animate.shift(1.45*RIGHT), series_aprx[0][21:23].animate.set_color(WHITE), values[2][0][1:].animate.set_color(WHITE),series_aprx[0][30].animate.set_color(YELLOW), values[3][0][1:].animate.set_color(YELLOW))
            self.wait()
            self.play(rect_f.animate.shift(0.72*DOWN), rect_t.animate.shift(1.45*RIGHT), series_aprx[0][30].animate.set_color(WHITE), values[3][0][1:].animate.set_color(WHITE),series_aprx[0][38].animate.set_color(YELLOW), values[4][0][1:].animate.set_color(YELLOW))
            self.wait()
            # move the derivates rectangle back to the top
            self.play(rect_f.animate.shift(4*0.72*UP), values[4][0][1:].animate.set_color(WHITE), values[0][0][1:].animate.set_color(YELLOW))
            self.wait()
            self.play(rect_f.animate.shift(0.72*DOWN), rect_t.animate.shift(1.45*RIGHT), series_aprx[0][38].animate.set_color(WHITE), values[0][0][1:].animate.set_color(WHITE),series_aprx[0][46].animate.set_color(YELLOW), values[1][0][1:].animate.set_color(YELLOW))
            self.wait()
            self.play(rect_f.animate.shift(0.72*DOWN), rect_t.animate.shift(1.45*RIGHT), series_aprx[0][46].animate.set_color(WHITE), values[1][0][1:].animate.set_color(WHITE),series_aprx[0][54:56].animate.set_color(YELLOW), values[2][0][1:].animate.set_color(YELLOW))
            self.wait()
            self.play(rect_f.animate.shift(0.72*DOWN), rect_t.animate.shift(1.45*RIGHT), series_aprx[0][54:56].animate.set_color(WHITE), values[2][0][1:].animate.set_color(WHITE),series_aprx[0][63].animate.set_color(YELLOW), values[3][0][1:].animate.set_color(YELLOW))
            self.wait()

            # Fade out the rectangles and return the values to white
            self.play(FadeOut(rect_f), FadeOut(rect_t), values[3][0][1:].animate.set_color(WHITE), series_aprx[0][64].animate.set_color(WHITE))
            return series_aprx
        
        def v2():
            series_aprx = VGroup(MathTex(r"T(x)=").scale(0.7).to_edge(DOWN).shift(0.5*UP+6*LEFT))
            self.play(Write(series_aprx[0]))
            self.wait()

            for i in range(0, 8):
                t1 = MathTex(r"\frac{f^{\left(n\right)}\left(0\right)}{n!}\cdot x^{n}").scale(0.9)
                t1 = t1.shift(taylor_formula[0][10:].get_center()-t1.get_center())
                t1 = VGroup(taylor_formula[0][10:].copy())
                if i !=0:
                    plus = MathTex(r"+").scale(0.7).next_to(series_aprx[-1], direction=RIGHT, buff = 0.1).shift(0.02*DOWN)
                    self.play(FadeIn(plus))
                    series_aprx.add(plus)
                self.play(t1.animate.scale(0.7).next_to(series_aprx[-1], direction=RIGHT, buff = 0.1).shift(0.055*UP))
                self.wait()
                # replace n with value of i
                self.play(Transform(t1[0][2], MathTex(i).scale(0.5).next_to(t1[0][2], aligned_edge=LEFT, buff = 0, direction=0)),
                        Transform(t1[0][8], MathTex(i).scale(0.6).next_to(t1[0][8], aligned_edge=LEFT, buff = 0, direction=0).shift(0.05*UP+0.02*RIGHT)),
                        Transform(t1[0][12], MathTex(i).scale(0.5).next_to(t1[0][12], aligned_edge=LEFT, buff = 0, direction=0)))
                
                # draw rectagle around the nominator and the cos derivates at the top
                if i == 0:
                    rect_f = SurroundingRectangle(cos_func, color=GREEN_B, buff=0.15).stretch_to_fit_width(4.5).shift(RIGHT)
                    rect_t = SurroundingRectangle(t1[0][:7], color=GREEN_B, buff=0.075)
                    self.play(Create(rect_f), Create(rect_t))
                else:
                    rect_t = SurroundingRectangle(t1[0][:7], color=GREEN_B, buff=0.075)
                    if i == 5:
                        self.play(rect_f.animate.shift(4*0.72*UP))
                        self.wait()
                    self.play(Create(rect_t), rect_f.animate.shift(0.72*DOWN))
                self.wait()
                self.play(Transform(t1[0][:7], values[i][0][1:].copy().scale(0.7).next_to(t1[0][8], buff = 0.2, direction=UP)))
                self.wait()
                self.play(FadeOut(rect_t))
                self.wait()
                self.play(t1[0][-6].animate.stretch_to_fit_width(0.5).shift(0.25*LEFT), t1[0][:-6].animate.shift(0.25*LEFT), t1[0][8:-3].animate.shift(0.25*LEFT), t1[0][-3:].animate.shift(0.5*LEFT))
                self.wait()
                series_aprx.add(t1)
            
            # add ... at the end
            dots = MathTex(r"+\cdots").scale(0.7).next_to(series_aprx[-1], direction=RIGHT, buff = 0.1).shift(0.04*DOWN)
            self.play(Write(dots), Uncreate(rect_f))
            self.wait()
            series_aprx.add(dots)

            return series_aprx
            
        series_aprx = v2()
        
        # 3.2.3 Mark all the terms that are 0 with a red box and cross them out
        self.play(series_aprx[3][0][:1].animate.set_color(RED),
                series_aprx[7][0][:1].animate.set_color(RED),
                series_aprx[11][0][:1].animate.set_color(RED),
                series_aprx[15][0][:1].animate.set_color(RED)
        )
        self.wait()
        
        cross_out_lines = VGroup()
        def cross(mob, mob_num, start, end):
            # cross out mob from start to end
            cross_out_line = Line(start=mob[mob_num][:start].get_corner(LEFT)+0.1*LEFT+0.4*UP, end=mob[mob_num][end].get_corner(RIGHT)+0.4*DOWN, color=RED)
            cross_out_lines.add(cross_out_line)
            return Create(cross_out_line)

        # Cross out all term with 0 coefficient
        self.play(cross(series_aprx, 3, 1, -1),
                cross(series_aprx, 7, 1, -1),
                cross(series_aprx, 11, 1, -1),
                cross(series_aprx, 15, 1, -1))
        self.wait()
        # Fade out the terms with 0 coefficient and shift the rest accordingly to the left
        self.play(FadeOut(cross_out_lines), 
                FadeOut(series_aprx[2:4], series_aprx[6:8], series_aprx[10:12], series_aprx[14:16]),
                series_aprx[4:6].animate.shift(1.4*LEFT),
                series_aprx[8:10].animate.shift(2.8*LEFT),
                series_aprx[12:14].animate.shift(4.2*LEFT),
                series_aprx[16:].animate.shift(5.6*LEFT)
                )
        self.wait()

        # quickly mark the n=0 in the formula to say that we start counting at 0
        box = SurroundingRectangle(taylor_formula[0][7:10], color=RED_C, buff=0.15)
        self.play(Create(box))
        self.wait()

        # Mark each part of the sum with a brace
        brace_1 = Brace(series_aprx[1], direction=UP, buff=0.1)
        text_1 = brace_1.get_text("0. Summand").scale(0.4).shift(0.2*DOWN)
        brace_2 = Brace(series_aprx[5], direction=UP, buff=0.1)
        text_2 = brace_2.get_text("1. Summand").scale(0.4).shift(0.2*DOWN)
        brace_3 = Brace(series_aprx[9], direction=UP, buff=0.1)
        text_3 = brace_3.get_text("2. Summand").scale(0.4).shift(0.2*DOWN)
        brace_4 = Brace(series_aprx[13], direction=UP, buff=0.1)
        text_4 = brace_4.get_text("3. Summand").scale(0.4).shift(0.2*DOWN)

        self.play(GrowFromCenter(brace_1), Write(text_1))
        self.wait()
        self.play(Uncreate(box))
        self.wait()
        self.play(GrowFromCenter(brace_2), Write(text_2))
        self.wait()
        self.play(GrowFromCenter(brace_3), Write(text_3))
        self.wait()
        self.play(GrowFromCenter(brace_4), Write(text_4))
        self.wait()

        # Add a "n-th" summand after the tripple dots
        plus = MathTex(r"+").scale(0.7).next_to(series_aprx[-1], direction=RIGHT, buff = 0.15).shift(0*DOWN)
        nth_summand = MathTex(r"\frac{?}{?}\cdot ?").scale(0.7).next_to(plus, direction=RIGHT, buff = 0.3).shift(0.02*UP)
        nth_summand[0][1].stretch_to_fit_width(0.55)
        nth_summand[0][3:].shift(0.25*RIGHT)
        self.play(Write(plus), Write(nth_summand), lag_ratio=0.2)
        self.wait()
        brace_n = Brace(nth_summand, direction=UP, buff=0.1)
        text_n = brace_n.get_text("n-th Summand").scale(0.4).shift(0.2*DOWN)
        self.play(GrowFromCenter(brace_n), Write(text_n))
        self.wait()

        # Show x^n and n! with boxes to derive the formula for the n-th summand
        box_n = SurroundingRectangle(series_aprx[1][0][8], color=RED_C, buff=0.1)
        box_xn = SurroundingRectangle(series_aprx[1][0][11:], color=RED_C, buff=0.1)
        self.play(Create(box_n), Create(box_xn))
        self.wait()
        self.play(box_n.animate.shift(1.6*RIGHT), box_xn.animate.shift(1.6*RIGHT))
        self.wait()
        self.play(box_n.animate.shift(1.6*RIGHT), box_xn.animate.shift(1.6*RIGHT))
        self.wait()
        self.play(box_n.animate.shift(1.6*RIGHT), box_xn.animate.shift(1.6*RIGHT))
        self.wait()
        self.play(Uncreate(box_n), Uncreate(box_xn))
        self.wait()

        # replace the ? with the correct values
        self.play(Transform(nth_summand[0][2], MathTex(r"(2n)!").scale(0.5).next_to(nth_summand[0][2], aligned_edge=LEFT, buff = 0, direction=0).shift(0.175*LEFT)),
                Transform(nth_summand[0][4], MathTex(r"x^{2n}").scale(0.6).next_to(nth_summand[0][4], aligned_edge=LEFT, buff = 0, direction=0).shift(0.02*UP+0.05*RIGHT)),)
        self.wait()

        # mark the nominators (1s and -1s)
        box_nom = SurroundingRectangle(series_aprx[1][0][1], color=RED_C, buff=0.15)
        self.play(Create(box_nom))
        self.wait()
        self.play(Transform(box_nom, SurroundingRectangle(series_aprx[5][0][1:7], color=RED_C, buff=0.1)))
        self.wait()
        self.play(Transform(box_nom, SurroundingRectangle(series_aprx[9][0][1], color=RED_C, buff=0.1)))
        self.wait()
        self.play(Transform(box_nom, SurroundingRectangle(series_aprx[13][0][1:7], color=RED_C, buff=0.1)))
        self.wait()
        self.play(Uncreate(box_nom))
        self.wait()

        # replace the ? with the correct values
        self.play(Transform(nth_summand[0][0], MathTex(r"(-1)^{n}").scale(0.5).next_to(nth_summand[0][0], aligned_edge=LEFT, buff = 0, direction=0).shift(0.175*LEFT)),
                  Transform(brace_n, Brace(nth_summand, direction=UP, buff=0.1)), text_n.animate.shift(0.15*RIGHT))
        self.wait()

        # write down full cosine formula underneath Taylor Formula
        cos_formula = MathTex(r"cos(x)=\sum_{n=0}^{\infty}\frac{(-1)^{n}}{n!}\cdot x^{2n}").scale(0.9).next_to(taylor_formula, direction=DOWN, buff = 0.5)
        self.play(Write(cos_formula))
        self.wait()

        # Fade Out Everything but the cos formula and move the cos formula in the center of the screen
        self.play(FadeOut(VGroup(series_aprx, brace_1, brace_2, brace_3, brace_4, brace_n, text_1, text_2, text_3, text_4, text_n, plus, nth_summand, plus, brace_n, text_n, taylor_formula, cos_func, cos_fd, cos_sd, cos_td, cos_fod, recycle_arrow, equivalent_symbol, values[0], values[1], values[2], values[3], values[4])),
                cos_formula.animate.move_to([0,0,0]))

class RadiusOfConvergence(Scene):
    def value_of_nth_derivative_at_x(a: float, x: float, n: int) ->float:
        """Return the values of the n-th derivative at x of a function of the form
        1/(x^2+a)"""
        derivatives = {"0": lambda x,a: 1/(x**2+a)}

    def construct(self):
        axes = Axes(
            x_range = [-2,4.5,1],
            y_range = [-2.5,2.5,1],
            x_length = 12,
            y_length = 6,
            axis_config = {"include_tip": True, "color": BLUE, "include_numbers": True},
        ).shift(1*DOWN, 0.5*RIGHT)
        
        def setup_graph():
            global log_graph, log_label
            log_graph = axes.plot(lambda x: math.log(x), x_range=[0.01, 4.5, 0.01], color=GREEN_D)
            log_label = MathTex("f(x)=log(x)").set_color(GREEN_D).to_corner(UR).scale(0.8).shift(2*DOWN)
            self.play(FadeIn(axes))
            self.wait()
            self.play(Write(log_graph))
            self.play(Write(log_label))
            self.wait()
        
        def calculate_derivatives():
            text_scale = 0.75
            gap = 0.5
            function = MathTex("f(x)=log(x)").scale(text_scale).to_corner(UL)
            first_deriv = MathTex(r"f'(x)=\frac{1}{x}").scale(text_scale).next_to(function.get_corner(LEFT), direction=DOWN, aligned_edge=LEFT, buff = gap)
            second_deriv = MathTex(r"f''(x)=-\frac{1}{x^2}").scale(text_scale).next_to(first_deriv.get_corner(LEFT), direction=DOWN, aligned_edge=LEFT, buff = gap)
            third_deriv = MathTex(r"f'''(x)=\frac{1\cdot2}{x^3}").scale(text_scale).next_to(second_deriv.get_corner(LEFT), direction=DOWN, aligned_edge=LEFT, buff = gap)
            fourth_deriv = MathTex(r"f^{(4)}(x)=-\frac{1\cdot2\cdot3}{x^4}").scale(text_scale).next_to(third_deriv.get_corner(LEFT), direction=DOWN, aligned_edge=LEFT, buff = gap)
            result_arrow = Arrow(start=function.get_right(), end=function.get_right()+[2,0,0], color=RED, buff=0.1).scale(text_scale)
            nth_deriv_start = MathTex(r"f^{(n)}(x)=\cdots\frac{\cdots}{x^n}").scale(text_scale).next_to(result_arrow.get_corner(RIGHT), direction=RIGHT, buff = 0.1, aligned_edge=LEFT).shift(0.1*DOWN)
            
            self.play(Write(function))
            self.wait()
            self.play(Write(first_deriv))
            self.wait()
            self.play(Write(second_deriv))
            self.wait()
            self.play(Write(third_deriv))
            self.wait()
            self.play(Write(fourth_deriv))
            self.wait()

            ### marking stuff for understanding purposes

            # marking the denominator of the derivatives
            self.play(first_deriv[0][8].animate.set_color(RED))
            self.wait()
            self.play(first_deriv[0][8].animate.set_color(WHITE), second_deriv[0][10:12].animate.set_color(RED))
            self.wait()
            self.play(second_deriv[0][10:12].animate.set_color(WHITE), third_deriv[0][12:14].animate.set_color(RED))
            self.wait()
            self.play(third_deriv[0][12:14].animate.set_color(WHITE), fourth_deriv[0][15:17].animate.set_color(RED))
            self.wait()
            self.play(fourth_deriv[0][15:17].animate.set_color(WHITE))
            self.wait()
            self.play(Write(result_arrow))
            self.wait()
            self.play(Write(nth_deriv_start))
            self.wait()
            
            # marking the numerator of the derivatives
            self.play(first_deriv[0][6].animate.set_color(RED))
            self.wait()
            self.play(first_deriv[0][6].animate.set_color(WHITE), second_deriv[0][8].animate.set_color(RED))
            self.wait()
            self.play(second_deriv[0][8].animate.set_color(WHITE), third_deriv[0][8:11].animate.set_color(RED))
            self.wait()
            self.play(third_deriv[0][8:11].animate.set_color(WHITE), fourth_deriv[0][9:14].animate.set_color(RED))
            self.wait()
            self.play(fourth_deriv[0][9:14].animate.set_color(WHITE))
            self.wait()

            self.play(Transform(nth_deriv_start[0][11:14], MathTex(r"(n-1)!").scale(text_scale).next_to(nth_deriv_start[0][11:14].get_corner(LEFT), direction=RIGHT, buff = 0, aligned_edge=LEFT)),
                    Transform(nth_deriv_start[0][14], MathTex(r"\frac{(n-1)!}{x^n}")[0][6].scale(text_scale).next_to(nth_deriv_start[0][14].get_corner(LEFT), direction=RIGHT, buff = 0, aligned_edge=LEFT)),
                    nth_deriv_start[0][15:17].animate.shift((MathTex(r"\frac{(n-1)!}{x^n}")[0][6].scale(text_scale).next_to(nth_deriv_start[0][14].get_corner(LEFT), direction=RIGHT, buff = 0, aligned_edge=LEFT).get_x()-nth_deriv_start[0][15:17].get_x())*RIGHT))
            self.wait()

            # marking the sign of the derivatives
            self.play(second_deriv[0][7].animate.set_color(RED))
            self.wait()
            self.play(second_deriv[0][7].animate.set_color(WHITE))
            self.wait()
            self.play(fourth_deriv[0][8].animate.set_color(RED))
            self.wait()
            self.play(fourth_deriv[0][8].animate.set_color(WHITE))
            self.wait()

            self.play(Transform(nth_deriv_start[0][8:11], MathTex(r"(-1)^{n+1}").scale(text_scale).next_to(nth_deriv_start[0][8:11].get_corner(LEFT), direction=RIGHT, buff = 0, aligned_edge=LEFT)),
                    nth_deriv_start[0][11:].animate.shift((MathTex(r"(-1)^{n+1}").scale(text_scale).next_to(nth_deriv_start[0][8:11].get_corner(LEFT), direction=RIGHT, buff = 0, aligned_edge=LEFT).get_corner(RIGHT)[0]-nth_deriv_start[0][10].get_corner(RIGHT)[0])*RIGHT))
            self.wait()
            
            # Fade Out most stuff, move nth_deriv to the top left and then create taylor approximation formula
            self.play(AnimationGroup(FadeOut(VGroup(function, first_deriv, second_deriv, third_deriv, fourth_deriv, result_arrow)), nth_deriv_start.animate.to_corner(UL), lag_ratio=0.5))
            self.wait()
            result_arrow = Arrow(start=nth_deriv_start.get_corner(RIGHT), end=nth_deriv_start.get_corner(RIGHT)+[1.8,0,0], color=RED, buff=0.1).scale(text_scale)
            text_scale = text_scale *0.93
            taylor_formula = MathTex(r"T(x)=\sum_{n=0}^{\infty}\frac{f^{\left(n\right)}\left(a\right)}{n!}\cdot (x-a)^{n}").scale(text_scale).next_to(result_arrow.get_corner(RIGHT), direction=RIGHT, buff = 0.15, aligned_edge=LEFT)
            self.play(AnimationGroup(Write(result_arrow), Write(taylor_formula), lag_ratio=0.5))
            self.wait()

            # Replace the a with 1 and the x with 1 in the nth derivative formula
            self.play(Transform(taylor_formula[0][24], MathTex(r"1").scale(text_scale).next_to(taylor_formula[0][24].get_corner(LEFT), aligned_edge=LEFT, buff = 0).shift(0.02*UP)),
                      Transform(taylor_formula[0][15], MathTex(r"1").scale(text_scale).next_to(taylor_formula[0][15].get_corner(LEFT), aligned_edge=LEFT, buff = 0).shift(0.01*UP+0.01*RIGHT)))
            self.wait()
            self.play(Transform(nth_deriv_start[0][5], MathTex(r"1").scale(text_scale).next_to(nth_deriv_start[0][5].get_corner(LEFT), direction=RIGHT, buff = 0, aligned_edge=LEFT).shift(0.02*UP+0.03*RIGHT)),
                        Transform(nth_deriv_start[0][15], MathTex(r"1").scale(text_scale).next_to(nth_deriv_start[0][15].get_corner(LEFT), direction=RIGHT, buff = 0, aligned_edge=LEFT))
                      )
            self.wait()
            dot = MathTex(r"\cdot").scale(text_scale).next_to(nth_deriv_start[0][8].get_corner(RIGHT), direction=RIGHT, buff = 0.15)
            self.play(FadeOut(nth_deriv_start[0][14:]), nth_deriv_start[0][9:14].animate.shift(0.275*DOWN+0.15*RIGHT), FadeIn(dot))
            self.wait()

            # draw a box around both f^(n)(1)
            box_f = SurroundingRectangle(nth_deriv_start[0][0:7], color=RED_C, buff=0.1)
            box_t = SurroundingRectangle(taylor_formula[0][10:17], color=RED_C, buff=0.1)
            self.play(Create(box_f), Create(box_t))
            self.wait()
            self.play(Transform(box_f, SurroundingRectangle(nth_deriv_start[0][8:], color=RED_C, buff=0.1).shift(0.15*UP)))
            self.wait()
            self.play(FadeOut(box_t))
            self.wait()
            expression_to_move = VGroup(nth_deriv_start[0][8:14].copy(), MathTex(r"\cdot").scale(text_scale).next_to(nth_deriv_start[0][8].get_corner(RIGHT), direction=RIGHT, buff = 0.15))
            self.play(AnimationGroup(AnimationGroup(
                        Transform(taylor_formula[0][17], MathTex(r"\frac{\left(-1\right)^{n+1}\cdot\left(n-1\right)!}{1}")[0][14].scale(text_scale).next_to(taylor_formula[0][17].get_corner(LEFT), direction=RIGHT, buff = 0, aligned_edge=LEFT)),
                        taylor_formula[0][18:20].animate.shift(0.8*RIGHT),
                        taylor_formula[0][20:].animate.shift(1.6*RIGHT),
                        FadeOut(taylor_formula[0][10:17])),
                      expression_to_move.animate.move_to(MathTex(r"\left(-1\right)^{n+1}\cdot\left(n-1\right)!").scale(text_scale).next_to(taylor_formula[0][10:17].get_corner(LEFT), direction=RIGHT, buff = 0, aligned_edge=LEFT).get_center()+0.15*DOWN)),
                      lag_ratio=0.5)
            self.wait()
            self.play(FadeOut(box_f))
            self.wait()

            # show that for n=0 the f^(n)(1) fails.
            # draw box around n=0
            box_n_0 = SurroundingRectangle(taylor_formula[0][7:10], color=RED_C, buff=0.1)
            self.play(Create(box_n_0))
            self.wait()
            # Create expression with n=0 on the left
            expression_n_0 = MathTex(r"f^{(0)}(1)=(-1)^{0+1}\cdot(0-1)!").scale(text_scale).next_to(nth_deriv_start.get_corner(LEFT), direction=DOWN, buff = 0.15, aligned_edge=LEFT)
            self.play(Write(expression_n_0))
            self.wait()
            # Transform the expression to -1 * (-1)! and cross it out
            self.play(Transform(expression_n_0, MathTex(r"f^{(0)}(1)=-1\cdot(-1)!").scale(text_scale).next_to(nth_deriv_start.get_corner(LEFT), direction=DOWN, buff = 0.15, aligned_edge=LEFT)))
            self.wait()
            cross_out_line = Line(start=expression_n_0[0][0].get_corner(LEFT)+0.1*LEFT+0.4*DOWN, end=expression_n_0[0][-1].get_corner(RIGHT)+0.4*UP+0.1*RIGHT, color=RED)
            self.play(Create(cross_out_line))
            self.wait()
            self.play(FadeOut(cross_out_line), FadeOut(expression_n_0), FadeOut(box_n_0))
            self.wait()

            # fix the formula on the right
            # add f^(0)(x)= infront and log label and draw box around the log(x)
            f_0_x = MathTex(r"f^{(0)}(x)=").scale(0.8).next_to(log_label[0][0], direction=LEFT, buff = 0.25, aligned_edge=RIGHT)
            self.play(Write(f_0_x))
            self.wait()
            box_log = SurroundingRectangle(log_label[0][5:], color=RED_C, buff=0.1)
            self.play(Create(box_log))
            self.wait()
            # add log(1) + between = sign and the formula
            addition = MathTex(r"log(1)+").scale(text_scale).next_to(taylor_formula[0][4].get_corner(RIGHT), direction=RIGHT, buff = 0.1, aligned_edge=LEFT)
            self.play(AnimationGroup(AnimationGroup(
                                        Transform(taylor_formula[0][9], MathTex(r"1").scale(text_scale-0.2).next_to(taylor_formula[0][9].get_corner(LEFT), direction=RIGHT, buff = 0, aligned_edge=LEFT).shift(1.12*RIGHT)),
                                        taylor_formula[0][5:9].animate.shift(1.12*RIGHT), 
                                        taylor_formula[0][17:].animate.shift(1.12*RIGHT),
                                        expression_to_move.animate.shift(1.12*RIGHT)
                                        ),
                                    Write(addition)), lag_ratio=0.5)
            self.wait()
            # transform log(1) to 0
            self.play(Uncreate(box_log), FadeOut(f_0_x), Transform(addition[0][:-1], MathTex(r"0").scale(text_scale).next_to(addition[0][:-1].get_corner(ORIGIN), direction=0, buff = 0, aligned_edge=ORIGIN)))
            self.wait()
            self.play(FadeOut(addition), taylor_formula[0][5:10].animate.shift(1.12*LEFT), taylor_formula[0][17:].animate.shift(1.12*LEFT), expression_to_move.animate.shift(1.12*LEFT))
            self.wait()
            # transform n! to (n-1)!*n
            self.play(Transform(taylor_formula[0][18:20], MathTex(r"(n-1)!\cdot n").scale(text_scale).next_to(taylor_formula[0][18].get_corner(ORIGIN), direction=0, buff = 0, aligned_edge=ORIGIN)))
            self.wait()
            # cross out (n-1)!
            cross_out_line1 = Line(start=taylor_formula[0][18].get_corner(LEFT)+0.1*LEFT+0.2*DOWN, end=taylor_formula[0][18].get_corner(RIGHT)+0.2*UP+0.3*LEFT, color=RED)
            cross_out_line2 = Line(start=expression_to_move[0][3].get_corner(LEFT)+0.1*LEFT+0.2*DOWN, end=expression_to_move[0][3].get_corner(RIGHT)+0.2*UP+0.1*RIGHT, color=RED)
            self.play(Create(cross_out_line1), Create(cross_out_line2))
            self.wait()
            self.play(FadeOut(cross_out_line1), FadeOut(cross_out_line2), FadeOut(taylor_formula[0][18][:-1]), FadeOut(expression_to_move[0][3]), FadeOut(expression_to_move[1]), 
                      taylor_formula[0][18][-1].animate.shift(1.4*LEFT),
                      Transform(taylor_formula[0][17], MathTex(r"\frac{\left(-1\right)^{n+1}}{1}")[0][7].scale(text_scale).next_to(taylor_formula[0][17].get_corner(LEFT), direction=RIGHT, buff = 0, aligned_edge=LEFT)),
                      taylor_formula[0][19:].animate.shift(1.4*LEFT))


            # Start the approximation with n terms
            for i in range(11):
                func = taylor_approximation(math.log, i, 1)
                # graph the function
                if i == 0:
                    graph = axes.plot(func, x_range=[0.01, 4.5, 0.01], color=ORANGE)
                    self.play(Write(graph), Transform(taylor_formula[0][5], MathTex(i).scale(0.5).next_to(taylor_formula[0][5].get_center(), direction=0, buff = 0.0, aligned_edge=ORIGIN)))
                else:
                    self.play(Transform(graph, axes.plot(func, x_range=[0.01, 4.5, 0.01], color=ORANGE)), Transform(taylor_formula[0][5], MathTex(i).scale(0.5).next_to(taylor_formula[0][5].get_center(), direction=0, buff = 0.0, aligned_edge=ORIGIN)))
                self.wait()
            
            # run a point along the originial log_graph from x=0 to x=2
            point = Dot(axes.coords_to_point(0.01, -1000), color=LIGHT_PINK)
            self.play(Create(point))
            self.wait()
            self.play(MoveAlongPath(point, axes.plot(lambda x: math.log(x), x_range=[0.1,2,0.1]), rate_func=linear))
            self.wait()

            # add a Brace from x=0 to x=2 to show the Interval of Convergence has size 2
            brace = BraceBetweenPoints(axes.coords_to_point(0,0), axes.coords_to_point(2,0), direction=UP, color=RED)
            text = brace.get_text("Interval of Convergence = (0,2)").scale(0.5).shift(0.2*DOWN).add_background_rectangle()
            self.play(GrowFromCenter(brace), Write(text))
            self.wait()

            # add vertical line at x=1 and at x=2 to show the Radius of Convergence
            line_1 = axes.get_vertical_line(axes.coords_to_point(1,0), color=RED)
            line_2 = axes.get_vertical_line(axes.coords_to_point(2,0), color=RED)
            self.play(Create(line_1), Create(line_2))
            self.wait()

            # add a brace to show the Radius of Convergence
            brace_2 = BraceBetweenPoints(axes.coords_to_point(1,0), axes.coords_to_point(2,0), direction=DOWN, color=RED_D)
            text_2 = brace_2.get_text("Radius of Convergence = 1").scale(0.5)
            self.play(GrowFromCenter(brace_2), Write(text_2))
            self.wait()
            
            # Fade out everything except the graph and the axes
            self.play(FadeOut(taylor_formula[0][:10]), FadeOut(taylor_formula[0][17]), FadeOut(taylor_formula[0][18][-1]), FadeOut(taylor_formula[0][19:]),
                      FadeOut(point), FadeOut(graph), FadeOut(brace), FadeOut(text), FadeOut(brace_2), FadeOut(text_2), FadeOut(dot), FadeOut(line_1),
                      FadeOut(line_2), FadeOut(brace), FadeOut(text), FadeOut(nth_deriv_start[0][:-3]), FadeOut(result_arrow), FadeOut(expression_to_move[0][:3]))
            self.wait()

            # rewrite original taylor formula 
            taylor_formula = MathTex(r"T(x)=\sum_{n=0}^{\infty}\frac{f^{\left(n\right)}\left(a\right)}{n!}\cdot (x-a)^{n}").scale(text_scale).to_corner(UR)
            self.play(Write(taylor_formula))
            
            # add Dot at (2,log(2)) and transform a to 2
            dot_2 = Dot(axes.coords_to_point(2, math.log(2)), color=LIGHT_PINK)
            self.play(Create(dot_2), 
                      Transform(taylor_formula[0][24], MathTex(r"2").set_color(LIGHT_PINK).scale(text_scale).next_to(taylor_formula[0][24].get_corner(LEFT), aligned_edge=LEFT, buff = 0).shift(0.02*UP)),
                      Transform(taylor_formula[0][15], MathTex(r"2").set_color(LIGHT_PINK).scale(text_scale).next_to(taylor_formula[0][15].get_corner(LEFT), aligned_edge=LEFT, buff = 0).shift(0.01*UP+0.01*RIGHT)))
            self.wait()

            # Start the approximation with n terms
            for i in range(21):
                # graph the function
                if i == 0:
                    graph = axes.plot(lambda x: taylorseries_log(x, i), x_range=[0.01, 4.5, 0.01], color=ORANGE)
                    #Transform infinity to 0, color T(x) orange
                    self.play(Transform(taylor_formula[0][5], MathTex(i).scale(0.5).next_to(taylor_formula[0][5].get_center(), direction=0, buff = 0.0, aligned_edge=ORIGIN)),
                              taylor_formula[0][:4].animate.set_color(ORANGE))
                    self.wait()
                    self.play(Write(graph))
                else:
                    self.play(Transform(graph, axes.plot(lambda x: taylorseries_log(x, i), x_range=[0.01, 4.5, 0.01], color=ORANGE)),
                              Transform(taylor_formula[0][5], MathTex(i).scale(0.5).next_to(taylor_formula[0][5].get_center(), direction=0, buff = 0.0, aligned_edge=ORIGIN)))
                self.wait()

            # show interval and radius again. This time its (0,4) and the radius is 2
            brace = BraceBetweenPoints(axes.coords_to_point(0,0), axes.coords_to_point(4,0), direction=UP, color=RED)
            text = brace.get_text("Convergence Interval = (0,4)").scale(0.5).shift(0.2*DOWN).add_background_rectangle()
            self.play(GrowFromCenter(brace), Write(text))
            self.wait()
            brace_2 = BraceBetweenPoints(axes.coords_to_point(2,0), axes.coords_to_point(4,0), direction=DOWN, color=RED_D)
            text_2 = brace_2.get_text("Radius of Convergence = 2").scale(0.5)
            self.play(GrowFromCenter(brace_2), Write(text_2))
            self.wait()

            # Store elements to fade later if needed
            self.convergence_elements = VGroup(interval_brace, interval_text, radius_brace, radius_text, term_counter)


        

            
        setup_graph()
        calculate_derivatives()

class RadiusOfConvergence_v2(Scene):
    def value_of_nth_derivative_at_x(a: float, x: float, n: int) ->float:
        """Return the values of the n-th derivative at x of a function of the form
        1/(x^2+a)"""
        derivatives = {"0": lambda x,a: 1/(x**2+a)}

    def construct(self):
        axes = Axes(
            x_range = [-2, 4.5, 1],
            y_range = [-2.5, 2.5, 1],
            x_length = 12,
            y_length = 6,
            axis_config = {"include_tip": True, "color": BLUE, "include_numbers": True},
        ).shift(1*DOWN + 0.5*RIGHT) # Adjusted shift slightly

        # --- Storing graph and label as instance variables ---
        self.log_graph = VMobject()
        self.log_label = VMobject()
        self.axes = axes
        self.approx_graph = VMobject() # To hold the current approximation graph
        self.taylor_formula_display = VMobject() # To hold the taylor formula text
        self.dot_a = VMobject() # To hold the dot at center 'a'


        def setup_graph():
            # Use self. variables
            self.log_graph = self.axes.plot(lambda x: math.log(x), x_range=[0.01, 4.5, 0.01], color=GREEN_D)
            self.log_label = MathTex("f(x)=\ln(x)").set_color(GREEN_D).to_corner(UR).scale(0.8).shift(2*DOWN) # Use ln instead of log
            self.play(FadeIn(self.axes))
            self.wait()
            self.play(Create(self.log_graph)) # Use Create for graphs
            self.play(Write(self.log_label))
            self.wait()

        # --- calculate_derivatives function (modified slightly for clarity/flow) ---
        def calculate_derivatives(center_a=1):
            # Ensure previous approximation is faded out if recalculating
            self.play(FadeOut(self.approx_graph, self.taylor_formula_display, self.dot_a))

            text_scale = 0.7
            gap = 0.4
            deriv_group = VGroup() # Group to hold derivatives

            function = MathTex(r"f(x)=\ln(x)").scale(text_scale).to_corner(UL)
            first_deriv = MathTex(r"f'(x)=\frac{1}{x}").scale(text_scale).next_to(function, DOWN, aligned_edge=LEFT, buff = gap)
            second_deriv = MathTex(r"f''(x)=-\frac{1}{x^2}").scale(text_scale).next_to(first_deriv, DOWN, aligned_edge=LEFT, buff = gap)
            third_deriv = MathTex(r"f'''(x)=\frac{2}{x^3}").scale(text_scale).next_to(second_deriv, DOWN, aligned_edge=LEFT, buff = gap) # Simplified 1*2
            fourth_deriv = MathTex(r"f^{(4)}(x)=-\frac{6}{x^4}").scale(text_scale).next_to(third_deriv, DOWN, aligned_edge=LEFT, buff = gap) # Simplified 1*2*3
            
            deriv_group.add(function, first_deriv, second_deriv, third_deriv, fourth_deriv)

            nth_deriv_final = MathTex(r"f^{(n)}(x)=(-1)^{n+1}\frac{(n-1)!}{x^n}", tex_template=TexTemplateLibrary.ctex).scale(text_scale) # Using ctex for better rendering maybe
            #nth_deriv_final_eval = MathTex(r"f^{(n)}(", str(center_a), r")=(-1)^{n+1}\frac{(n-1)!}{", str(center_a), r"^n}").scale(text_scale)
            eval_tex_string = rf"f^{{(n)}}({center_a})=(-1)^{{n+1}}\frac{{(n-1)!}}{{{center_a}^n}}"
            nth_deriv_final_eval = MathTex(eval_tex_string, tex_template=TexTemplateLibrary.ctex).scale(text_scale) # Keep ctex template if needed

            # Use a temporary simplified version for the build-up animation
            nth_deriv_start = MathTex(r"f^{(n)}(x)=\cdots\frac{\cdots}{x^n}").scale(text_scale).next_to(fourth_deriv, DOWN, aligned_edge=LEFT, buff=gap*1.5)

            self.play(Write(function))
            self.wait(0.5)
            self.play(Write(first_deriv))
            self.wait(0.5)
            self.play(Write(second_deriv))
            self.wait(0.5)
            self.play(Write(third_deriv))
            self.wait(0.5)
            self.play(Write(fourth_deriv))
            self.wait()

            # Highlighting parts - Condensed this part for brevity
            # Denominator
            highlights_denom = [first_deriv[0][7], second_deriv[0][9:11], third_deriv[0][9:11], fourth_deriv[0][11:13]]
            for i in range(len(highlights_denom)):
                self.play(highlights_denom[i].animate.set_color(RED), run_time=0.5)
                self.wait(0.2)
                if i < len(highlights_denom) - 1:
                    self.play(highlights_denom[i].animate.set_color(WHITE), run_time=0.5)
                else: # Last one
                    self.play(Write(nth_deriv_start[-2:]), run_time=0.5) # Show x^n part
                    self.play(highlights_denom[i].animate.set_color(WHITE), run_time=0.5)
            self.wait(0.5)

            # Numerator (Factorial part)
            highlights_num = [first_deriv[0][5], second_deriv[0][7], third_deriv[0][7], fourth_deriv[0][9]] # Simplified factorials
            targets_num_text = [r"0!", r"1!", r"2!", r"3!"]
            temp_num = VGroup()
            for i in range(len(highlights_num)):
                 # Create target text to measure final position (using (n-1)!)
                target_factorial = MathTex("(n-1)!").scale(text_scale).move_to(nth_deriv_start[0][11:14], aligned_edge=LEFT)
                temp_tex = MathTex(targets_num_text[i]).scale(text_scale).move_to(highlights_num[i])
                temp_num.add(temp_tex)
                self.play(Transform(highlights_num[i], temp_tex), run_time=0.5)
                self.wait(0.2)
                if i < len(highlights_num) - 1:
                     self.play(FadeOut(highlights_num[i]), run_time=0.5) # Fade out previous number
                else: # Last one
                    self.play(Transform(temp_num, target_factorial), run_time=0.5) # Transform group into (n-1)!
                    self.play(Write(nth_deriv_start[0][8:11]), # Write dots
                              Write(nth_deriv_start[0][14])) # Write fraction line
            self.wait(0.5)

            # Sign
            highlights_sign = [second_deriv[0][6], fourth_deriv[0][8]] # Minus signs
            # Create target text to measure final position
            target_sign = MathTex("(-1)^{n+1}").scale(text_scale).move_to(nth_deriv_start[0][8:11], aligned_edge=RIGHT)
            sign_group = VGroup()
            for i in range(len(highlights_sign)):
                sign_group.add(highlights_sign[i])
                self.play(highlights_sign[i].animate.set_color(YELLOW), run_time=0.5)
                self.wait(0.2)
                if i < len(highlights_sign) -1:
                    self.play(highlights_sign[i].animate.set_color(WHITE), run_time=0.5)
                else: # Last one
                    # Transform the existing signs and dots into the final sign term
                     self.play(Transform(sign_group, target_sign), run_time=0.5)
                     self.play(Write(nth_deriv_start[0][5:8])) # Write f^(n)(x)=
            self.wait(0.5)
            
            # Transform the built-up version to the final nth derivative formula
            nth_deriv_final.move_to(nth_deriv_start)
            self.play(Transform(nth_deriv_start, nth_deriv_final), FadeOut(temp_num), FadeOut(sign_group))
            self.wait()

            # Fade out calculation steps, move nth derivative formula up
            self.play(FadeOut(deriv_group), nth_deriv_start.animate.to_corner(UL).shift(0.5*DOWN))
            self.wait()

            # Show evaluated version f^(n)(a)
            nth_deriv_final_eval.next_to(nth_deriv_start, DOWN, buff=gap, aligned_edge=LEFT)
            self.play(Write(nth_deriv_final_eval))
            self.wait()
            
            # General Taylor Formula
            taylor_formula_gen = MathTex(r"T(x)=\sum_{n=0}^{\infty}\frac{f^{(n)}(a)}{n!}(x-a)^n").scale(text_scale).next_to(nth_deriv_final_eval, DOWN, buff=gap*1.5, aligned_edge=LEFT)
            self.play(Write(taylor_formula_gen))
            self.wait()

            # Substitute a = center_a
            specific_tex_string = rf"T(x)=\sum_{{n=0}}^{{\infty}}\frac{{f^{{(n)}}({center_a})}}{{n!}}(x-{center_a})^n"
            taylor_formula_specific = MathTex(specific_tex_string).scale(text_scale).move_to(taylor_formula_gen)
            self.play(Transform(taylor_formula_gen, taylor_formula_specific))
            self.wait()

            # Substitute the expression for f^(n)(a) - requires care with n=0
            # Box f^(n)(a) parts
            box_eval = SurroundingRectangle(nth_deriv_final_eval[0][4:], color=RED_C, buff=0.05)
            box_taylor = SurroundingRectangle(taylor_formula_gen[0][10:17], color=RED_C, buff=0.05) # Adjust indices based on a
            self.play(Create(box_eval), Create(box_taylor))
            self.wait()

            # Explicitly handle n=0 case
            text_n0_issue = Tex(r"$f^{(0)}(a) = \ln(a)$", font_size=24).next_to(taylor_formula_gen, DOWN, buff=0.5).set_color(YELLOW)
            text_n_formula_issue = Tex(r"Formula requires $n \geq 1$", font_size=24).next_to(text_n0_issue, DOWN).set_color(YELLOW)
            self.play(Write(text_n0_issue))
            self.play(Write(text_n_formula_issue))
            self.wait(1.5)

            # Modify Taylor sum to start from n=1 and add f(a) separately
            # taylor_final_form = MathTex(
            #     r"T(x) = f(", str(center_a), r") + \sum_{n=1}^{\infty}", # Term 0
            #     r"\frac{(-1)^{n+1}(n-1)!}{", str(center_a), r"^n \cdot n!}", # Substituted f^(n)(a)/n!
            #     r"(x-", str(center_a), r")^n" # (x-a)^n part
            # ).scale(text_scale).move_to(taylor_formula_gen).shift(0.1*DOWN) # Shift slightly to avoid overlap
            taylor_final_form = MathTex(
                rf"T(x) = f({center_a}) + \sum_{{n=1}}^{{\infty}}",           # Part 0 (f(a) term + sum start)
                rf"\frac{{(-1)^{{n+1}}(n-1)!}}{{{center_a}^n \cdot n!}}",    # Part 1 (General term fraction before simplification)
                rf"(x-{center_a})^n"                                         # Part 2 ((x-a)^n term)
            ).scale(text_scale).move_to(taylor_formula_gen).shift(0.1*DOWN)

            # Simplify n! = n * (n-1)! and cancel
            taylor_simplified = MathTex(
                rf"T(x) = \ln({center_a}) + \sum_{{n=1}}^{{\infty}}",        # Part 0 (ln(a) term + sum start)
                rf"\frac{{(-1)^{{n+1}}}}{{{center_a}^n \cdot n}}",         # Part 1 (Simplified fraction)
                rf"(x-{center_a})^n"                                      # Part 2 ((x-a)^n term)
            ).scale(text_scale).move_to(taylor_final_form)

            self.play(FadeOut(box_eval, box_taylor, text_n0_issue, text_n_formula_issue))
            self.play(Transform(taylor_formula_gen, taylor_final_form))
            self.wait(1)
            # Show cancellation
            term_to_simplify = taylor_final_form[1]
            cancel_line1 = Line(term_to_simplify[6:11].get_corner(UL), term_to_simplify[6:11].get_corner(DR), color=RED, stroke_width=2) # (n-1)!
            cancel_line2 = Line(term_to_simplify[-3:-1].get_corner(UL), term_to_simplify[-3:-1].get_corner(DR), color=RED, stroke_width=2) # n! -> n (n-1)!
            n_only = MathTex("n").scale(text_scale).move_to(term_to_simplify[-2]).shift(0.1*LEFT) # Just the 'n' remains
            self.play(Create(cancel_line1), Create(cancel_line2))
            self.wait(0.5)
            self.play(FadeOut(cancel_line1, cancel_line2))
            self.play(Transform(taylor_formula_gen, taylor_simplified)) # Transform to simplified version
            self.wait(1)

            # Clean up derivative formulas
            self.play(FadeOut(nth_deriv_start, nth_deriv_final_eval))
            # Move final formula to top right
            self.taylor_formula_display = taylor_formula_gen # Store handle
            self.play(self.taylor_formula_display.animate.scale(0.8).to_corner(UR))
            self.wait()

            # --- Approximation Visualization ---
            max_terms = 20 if center_a > 1 else 10 # Use more terms for larger 'a' if needed
            
            # Dot at center 'a'
            self.dot_a = Dot(self.axes.c2p(center_a, math.log(center_a)), color=YELLOW)
            self.play(Create(self.dot_a))
            self.wait(0.5)

            # Store graph handle in self.approx_graph
            self.approx_graph = self.axes.plot(lambda x: taylorseries_log(x, 0, a=center_a), x_range=[0.01, 4.5, 0.01], color=ORANGE)
            term_counter = MathTex("N=0").scale(0.7).next_to(self.taylor_formula_display, DOWN, buff=0.2, aligned_edge=RIGHT)

            self.play(
                Create(self.approx_graph),
                Write(term_counter),
                self.taylor_formula_display[0][:4].animate.set_color(ORANGE), # Color T(x)
            )
            self.wait(0.5)

            for i in range(1, max_terms + 1):
                new_graph = self.axes.plot(lambda x: taylorseries_log(x, i, a=center_a), x_range=[0.01, 4.5, 0.01], color=ORANGE)
                new_term_counter = MathTex(f"N={i}").scale(0.7).move_to(term_counter)
                self.play(
                    Transform(self.approx_graph, new_graph),
                    Transform(term_counter, new_term_counter),
                    run_time=0.5 # Faster updates
                )
                # Add very short pauses for higher terms
                self.wait(0.1 if i > 5 else 0.25)

            self.wait(1)

            # --- Show Interval and Radius ---
            interval_start = 0
            interval_end = 2 * center_a
            radius = center_a

            # Ensure axes cover the interval
            if interval_end > self.axes.x_range[1]:
                 print(f"Warning: Interval ({interval_start}, {interval_end}) exceeds axes range.")
                 interval_end = self.axes.x_range[1] # Clamp to axes limit visually

            interval_brace = BraceBetweenPoints(self.axes.c2p(interval_start, 0), self.axes.c2p(interval_end, 0), direction=UP, color=RED)
            interval_text = interval_brace.get_text(f"Converges on ({interval_start}, {interval_end})").scale(0.6).shift(0.1*DOWN) # Adjusted size/pos

            radius_brace = BraceBetweenPoints(self.axes.c2p(center_a, 0), self.axes.c2p(interval_end, 0), direction=DOWN, color=YELLOW)
            radius_text = radius_brace.get_text(f"Radius R = {radius}").scale(0.6)

            self.play(GrowFromCenter(interval_brace), Write(interval_text))
            self.wait(0.5)
            self.play(GrowFromCenter(radius_brace), Write(radius_text))
            self.wait(2)
            
            # Store elements to fade later if needed
            self.convergence_elements = VGroup(interval_brace, interval_text, radius_brace, radius_text, term_counter)
            self.play(FadeOut(self.convergence_elements, self.approx_graph, self.taylor_formula_display, self.dot_a))


        def show_general_radius():
            # Fade out previous specific elements (a=2 case)
            self.play(FadeOut(self.convergence_elements, self.approx_graph, self.taylor_formula_display, self.dot_a))
            self.wait()

            # Title
            title = Tex("General Case: Radius of Convergence for $f(x)=\ln(x)$", font_size=36).to_edge(UP)
            self.play(Write(title))

            # Singularity at x=0
            singularity_pt = self.axes.c2p(0, 0) # Point on axis
            singularity_line = DashedLine(
                self.axes.c2p(0, self.axes.y_range[0]),
                self.axes.c2p(0, self.axes.y_range[1]),
                color=RED,
                stroke_width=3
            )
            singularity_label = Tex("Singularity!", color=RED, font_size=28).next_to(self.axes.c2p(0, 1.5), RIGHT, buff=0.1)
            self.play(Create(singularity_line), Write(singularity_label))
            self.wait(1)

            # General center 'a' using ValueTracker
            a_val = ValueTracker(1.5) # Start at a generic point

            a_dot = Dot(color=YELLOW, radius=0.08)
            a_label = MathTex("a", color=YELLOW).scale(0.8)
            
            # Updaters to move dot and label with 'a_val'
            a_dot.add_updater(lambda m: m.move_to(self.axes.c2p(a_val.get_value(), 0)))
            a_label.add_updater(lambda m: m.next_to(a_dot, DOWN, buff=0.15))

            self.play(Create(a_dot), Write(a_label))
            self.wait(0.5)

            # Line representing the radius from 'a' to singularity
            radius_line = Line(color=YELLOW, stroke_width=5)
            radius_line.add_updater(lambda m: m.put_start_and_end_on(
                self.axes.c2p(a_val.get_value(), 0), # Start at 'a' on axis
                singularity_pt # End at singularity
            ))

            # Brace for the radius
            radius_brace = Brace(radius_line, direction=DOWN, color=YELLOW)
            radius_text = MathTex("R = a", color=YELLOW).scale(0.7)

            # Updater for brace and text
            def radius_updater(mob):
                mob.become(Brace(radius_line, direction=DOWN, color=YELLOW))
                radius_text.next_to(radius_brace, DOWN, buff=0.1)
            radius_brace.add_updater(radius_updater)
            radius_text.add_updater(lambda m: m.next_to(radius_brace, DOWN, buff=0.1))


            self.play(Create(radius_line))
            self.play(GrowFromCenter(radius_brace), Write(radius_text))
            self.wait(1)

            # Brace for the interval (0, 2a)
            # interval_brace = Brace(color=BLUE)
            interval_brace = VMobject()
            interval_text = MathTex("(0, 2a)", color=BLUE).scale(0.7)
            
            # Updater for interval
            def interval_updater(mob):
                current_a = a_val.get_value()
                 # Clamp interval end to axes visually if needed
                end_x = min(2*current_a, self.axes.x_range[1]) 
                start_x = 1e-3 # Avoid exactly 0 for visual brace
                if end_x > start_x: # Ensure valid brace points
                     mob.become(BraceBetweenPoints(
                        self.axes.c2p(start_x, 0), 
                        self.axes.c2p(end_x, 0), 
                        direction=UP, color=BLUE
                        ))
                     interval_text.next_to(interval_brace, UP, buff=0.1)
                else: # If a is too small, hide brace/text
                    mob.become(VMobject()) # Become empty
                    interval_text.become(VMobject())

            interval_brace.add_updater(interval_updater)
            interval_text.add_updater(lambda m: m.next_to(interval_brace, UP, buff=0.1) if interval_brace.has_points() else m.become(VMobject()))


            self.play(GrowFromCenter(interval_brace), Write(interval_text))
            self.wait(1)

            # Animate 'a' changing
            explanation_text = Tex(
                "The distance from center 'a' to the singularity at $x=0$ determines the radius $R=a$.",
                font_size=28
            ).next_to(title, DOWN, buff=0.3)
            self.play(Write(explanation_text))
            self.wait(1)

            self.play(a_val.animate.set_value(1), run_time=2)
            self.wait(1)
            self.play(a_val.animate.set_value(2), run_time=2)
            self.wait(1)
            self.play(a_val.animate.set_value(0.5), run_time=2)
            self.wait(1)
            # Return to generic
            self.play(a_val.animate.set_value(1.5), run_time=1)
            self.wait(2)
            
            # Final Conclusion Text
            conclusion = Tex(
                r"The Taylor series for $\ln(x)$ centered at $a>0$ converges on the interval $(0, 2a)$.",
                font_size=32
            ).to_edge(DOWN, buff=0.5)
            self.play(Write(conclusion))
            self.wait(3)

            # Cleanup updaters before finishing
            a_dot.clear_updaters()
            a_label.clear_updaters()
            radius_line.clear_updaters()
            radius_brace.clear_updaters()
            radius_text.clear_updaters()
            interval_brace.clear_updaters()
            interval_text.clear_updaters()

            # Fade out general explanation elements
            self.play(FadeOut(title, singularity_line, singularity_label, a_dot, a_label, radius_line, radius_brace, radius_text, interval_brace, interval_text, explanation_text, conclusion))
            self.wait(1)
            # Optionally keep axes and log graph for the end
            self.play(FadeOut(self.log_label)) # Fade label if desired


        # --- Call the functions ---
        setup_graph()
        calculate_derivatives(center_a=1) # Run for a=1
        calculate_derivatives(center_a=2) # Run for a=2
        show_general_radius() # Run the new general explanation

        self.wait(2) # Hold final scene briefly

class RadiusOfConvergence_v3(Scene):
    def construct(self):
        axes = Axes(
            x_range = [-2, 4.5, 1],
            y_range = [-2.5, 2.5, 1],
            x_length = 12,
            y_length = 6,
            axis_config = {"include_tip": True, "color": BLUE, "include_numbers": True},
        ).shift(1*DOWN + 0.5*RIGHT) # Adjusted shift slightly

        # --- Instance variables for persistent/shared objects ---
        self.axes = axes
        self.log_graph = VMobject()
        self.log_label = VMobject()
        self.nth_deriv_formula_display = VMobject() # Will hold f^(n)(x) formula

        # --- Instance variables for objects specific to a center 'a' ---
        # These need to be cleaned up before showing the next 'a'
        self.approx_graph = VMobject()
        self.taylor_formula_display = VMobject() # Holds T(x) sum formula for current 'a'
        self.dot_a = VMobject()
        self.term_counter = VMobject()
        self.convergence_elements = VGroup() # Holds braces and text for interval/radius

        # --- Helper Functions ---
        def setup_graph():
            self.log_graph = self.axes.plot(lambda x: math.log(x), x_range=[0.01, 4.5, 0.01], color=GREEN_D)
            self.log_label = MathTex(r"f(x)=\ln(x)", color=GREEN_D).to_corner(UL).shift(DOWN*0.5 + RIGHT*0.5)
            self.play(FadeIn(self.axes))
            self.wait(0.5)
            self.play(Create(self.log_graph))
            self.play(Write(self.log_label))
            self.wait()

        def derive_nth_derivative():
            text_scale = 0.7
            gap = 0.4
            deriv_group = VGroup()

            # --- Derivatives Display ---
            function = MathTex(r"f(x)=\ln(x)").scale(text_scale).to_corner(UL).shift(DOWN*1.5)
            first_deriv = MathTex(r"f'(x)=\frac{1}{x}").scale(text_scale).next_to(function, DOWN, aligned_edge=LEFT, buff = gap)
            second_deriv = MathTex(r"f''(x)=-\frac{1}{x^2}").scale(text_scale).next_to(first_deriv, DOWN, aligned_edge=LEFT, buff = gap)
            third_deriv = MathTex(r"f'''(x)=\frac{2}{x^3}").scale(text_scale).next_to(second_deriv, DOWN, aligned_edge=LEFT, buff = gap)
            fourth_deriv = MathTex(r"f^{(4)}(x)=-\frac{6}{x^4}").scale(text_scale).next_to(third_deriv, DOWN, aligned_edge=LEFT, buff = gap)
            deriv_group.add(function, first_deriv, second_deriv, third_deriv, fourth_deriv)

            # --- Final nth Derivative Formula ---
            # Use f-string for correct parsing, ensure literal braces are doubled {{}}
            nth_deriv_tex = rf"f^{{(n)}}(x)=(-1)^{{n+1}}\frac{{(n-1)!}}{{x^n}}"
            nth_deriv_final = MathTex(nth_deriv_tex, tex_template=TexTemplateLibrary.ctex).scale(text_scale)

            # --- Build-up Animation ---
            self.play(Write(function))
            self.wait(0.5); self.play(Write(first_deriv))
            self.wait(0.5); self.play(Write(second_deriv))
            self.wait(0.5); self.play(Write(third_deriv))
            self.wait(0.5); self.play(Write(fourth_deriv))
            self.wait()

            # --- Highlighting and Transformation (Condensed) ---
            # Denominator x^n
            # Indices: f'[7], f''[9:11], f'''[9:11], f(4)[11:13] --> nth[-2:] ('x^n')
            anim_denom = Succession(
                Indicate(first_deriv[0][7], color=RED), Indicate(second_deriv[0][9:11], color=RED),
                Indicate(third_deriv[0][9:11], color=RED), Indicate(fourth_deriv[0][11:13], color=RED),
            )
            self.play(anim_denom)
            self.wait(0.5)

            # Numerator (n-1)!
            # Indices: f'[5] ('1'), f''[7] ('1'), f'''[7] ('2'), f(4)[9] ('6') --> nth[13:18] ('(n-1)!')
             # Note: Indices depend heavily on exact tex string rendering, might need adjustment
            anim_num = Succession(
                Indicate(first_deriv[0][5], color=YELLOW), Indicate(second_deriv[0][7], color=YELLOW),
                Indicate(third_deriv[0][7], color=YELLOW), Indicate(fourth_deriv[0][9], color=YELLOW),
            )
            self.play(anim_num)
            self.wait(0.5)

            # Sign (-1)^(n+1)
            # Indices: f''[6] ('-'), f(4)[8] ('-') --> nth[8:13] ('(-1)^{n+1}')
            anim_sign = Succession(
                 Indicate(second_deriv[0][6], color=BLUE), Indicate(fourth_deriv[0][8], color=BLUE)
            )
            self.play(anim_sign)
            self.wait(0.5)

            # Transform into the final formula
            nth_deriv_final.move_to(fourth_deriv, aligned_edge=LEFT).shift(DOWN * gap * 1.5)
            self.play(FadeOut(deriv_group), Write(nth_deriv_final))
            self.wait(1)

            # Move to corner and store
            self.nth_deriv_formula_display = nth_deriv_final # Store handle
            self.play(self.nth_deriv_formula_display.animate.to_corner(UL))
            self.wait()

        def show_taylor_for_center(center_a):
            text_scale = 0.7
            gap = 0.4

            # --- Cleanup from previous center (if any) ---
            # Check if the objects exist before trying to fade them out
            cleanup_targets = [self.approx_graph, self.taylor_formula_display, self.dot_a, self.term_counter]
            # VGroup might be empty, check elements
            if self.convergence_elements and len(self.convergence_elements) > 0:
                 cleanup_targets.append(self.convergence_elements)
            
            # Create a list of existing objects to fade
            objects_to_fade = [m for m in cleanup_targets if m and m.has_points()] # Check if VMobject is not empty

            if objects_to_fade:
                self.play(*[FadeOut(m) for m in objects_to_fade])
                # Reset convergence_elements to an empty VGroup after fading
                self.convergence_elements = VGroup() 
            self.wait(0.5)

            # --- Evaluate f^(n)(a) ---
            # Make sure nth_deriv_formula_display is visible (it should be in UL corner)
            self.play(FadeIn(self.nth_deriv_formula_display)) # Ensure it's visible if faded out accidentally

            # Indices in nth_deriv_tex: "f^{{(n)}}(x)=(-1)^{{n+1}}\\frac{{(n-1)!}}{{x^n}}"
            # Target 'x' in f^(n)(x) is index 5
            # Target 'x' in x^n is index 19
            eval_tex = rf"f^{{(n)}}({center_a})=(-1)^{{n+1}}\frac{{(n-1)!}}{{{center_a}^n}}"
            nth_deriv_eval = MathTex(eval_tex, tex_template=TexTemplateLibrary.ctex).scale(text_scale)
            nth_deriv_eval.next_to(self.nth_deriv_formula_display, DOWN, buff=gap, aligned_edge=LEFT)

            # Animate substitution
            x_in_fn = self.nth_deriv_formula_display[0][5]
            x_in_xn = self.nth_deriv_formula_display[0][19]
            a_label_fn = MathTex(str(center_a), color=YELLOW).scale(text_scale).move_to(x_in_fn)
            a_label_xn = MathTex(str(center_a), color=YELLOW).scale(text_scale).move_to(x_in_xn)

            self.play(Transform(x_in_fn, a_label_fn), Transform(x_in_xn, a_label_xn))
            self.wait(0.5)
            self.play(Write(nth_deriv_eval))
            self.wait(1)
            # Revert original formula back (or just fade out and recreate)
            self.play(FadeOut(x_in_fn, x_in_xn), FadeIn(self.nth_deriv_formula_display[0][5]), FadeIn(self.nth_deriv_formula_display[0][19])) # Restore original x's
            # self.remove(a_label_fn, a_label_xn) # Alternative cleanup


            # --- Taylor Formula Setup ---
            taylor_gen_tex = r"T(x)=\sum_{n=0}^{\infty}\frac{f^{(n)}(a)}{n!}(x-a)^n"
            taylor_gen_formula = MathTex(taylor_gen_tex).scale(text_scale).next_to(nth_deriv_eval, DOWN, buff=gap*1.5, aligned_edge=LEFT)
            self.play(Write(taylor_gen_formula))
            self.wait(0.5)

            # Substitute 'a'
            taylor_spec_tex = rf"T(x)=\sum_{{n=0}}^{{\infty}}\frac{{f^{{(n)}}({center_a})}}{{n!}}(x-{center_a})^n"
            taylor_spec_formula = MathTex(taylor_spec_tex).scale(text_scale).move_to(taylor_gen_formula)
            # Indices in taylor_gen_tex: f^(n)(a) is [10:17], (x-a) is [21:26] (a is 15 and 24)
            a_in_fn = taylor_gen_formula[0][15]
            a_in_xa = taylor_gen_formula[0][24]
            a_lab1 = MathTex(str(center_a), color=YELLOW).scale(text_scale).move_to(a_in_fn)
            a_lab2 = MathTex(str(center_a), color=YELLOW).scale(text_scale).move_to(a_in_xa)

            self.play(Transform(a_in_fn, a_lab1), Transform(a_in_xa, a_lab2))
            self.wait(0.5)
            self.play(Transform(taylor_gen_formula, taylor_spec_formula), FadeOut(a_in_fn, a_in_xa)) # Transform base formula
            # self.remove(a_lab1, a_lab2) # Alternative cleanup
            self.wait(1)

            # --- Substitute f^(n)(a) - Handle n=0 case ---
            text_n0_issue = Tex(r"$f^{(0)}(a) = \ln(a)$. Formula for $n \geq 1$.", font_size=24).next_to(taylor_gen_formula, DOWN, buff=0.5).set_color(YELLOW)
            self.play(Write(text_n0_issue))
            self.wait(1.5)

            # Corrected Taylor form (n=0 term + sum from n=1)
            # Using 3 parts for easier manipulation later
            final_form_part0 = rf"T(x) = \ln({center_a}) + \sum_{{n=1}}^{{\infty}}"
            final_form_part1 = rf"\frac{{(-1)^{{n+1}}(n-1)!}}{{{center_a}^n \cdot n!}}"
            final_form_part2 = rf"(x-{center_a})^n"
            taylor_final_form = MathTex(final_form_part0, final_form_part1, final_form_part2).scale(text_scale).move_to(taylor_gen_formula)

            # Box f^(n)(a) parts before transform
            # Indices in nth_deriv_eval: f^(n)(a)=... -> Value starts at index 7
            # Indices in taylor_spec_formula: f^(n)(a) part is roughly [10:17]
            box_eval = SurroundingRectangle(nth_deriv_eval[0][7:], color=RED_C, buff=0.05)
            box_taylor = SurroundingRectangle(taylor_gen_formula[0][10:17], color=RED_C, buff=0.05)
            self.play(Create(box_eval), Create(box_taylor))
            self.wait(1)

            self.play(FadeOut(box_eval, box_taylor, text_n0_issue))
            self.play(Transform(taylor_gen_formula, taylor_final_form))
            self.wait(1)

            # --- Simplify n! = n * (n-1)! ---
            term_to_simplify = taylor_final_form[1] # The fraction part
            # Find indices within term_to_simplify (part 1)
            # Example: rf"\frac{{(-1)^{{n+1}}(n-1)!}}{{{center_a}^n \cdot n!}}"
            # (n-1)! might be indices [13:18]
            # n! might be indices [-3:-1]
            # Use .index_labels() if unsure! Let's assume these indices:
            idx_n_minus_1_fact = (13, 18) # Guess, adjust if needed
            idx_n_fact = (-3, -1)         # Guess, adjust if needed

            if len(term_to_simplify[0]) > max(idx_n_minus_1_fact[1], abs(idx_n_fact[0])): # Basic check
                cancel_line1 = Line(term_to_simplify[0][idx_n_minus_1_fact[0]:idx_n_minus_1_fact[1]].get_corner(UL), term_to_simplify[0][idx_n_minus_1_fact[0]:idx_n_minus_1_fact[1]].get_corner(DR), color=RED, stroke_width=2)
                cancel_line2 = Line(term_to_simplify[0][idx_n_fact[0]:idx_n_fact[1]].get_corner(UL), term_to_simplify[0][idx_n_fact[0]:idx_n_fact[1]].get_corner(DR), color=RED, stroke_width=2)
                self.play(Create(cancel_line1), Create(cancel_line2))
                self.wait(1)
            else:
                print("WARNING: Indices for cancellation might be wrong. Skipping cancellation animation.")
                self.wait(1) # Still wait if skipping

            # Simplified Taylor form
            simpl_form_part0 = rf"T(x) = \ln({center_a}) + \sum_{{n=1}}^{{\infty}}"
            simpl_form_part1 = rf"\frac{{(-1)^{{n+1}}}}{{{center_a}^n \cdot n}}" # Simplified fraction
            simpl_form_part2 = rf"(x-{center_a})^n"
            taylor_simplified = MathTex(simpl_form_part0, simpl_form_part1, simpl_form_part2).scale(text_scale).move_to(taylor_final_form)

            # Fade out lines and transform
            if 'cancel_line1' in locals():
                 self.play(FadeOut(cancel_line1, cancel_line2))
            self.play(Transform(taylor_gen_formula, taylor_simplified))
            self.wait(1)

            # --- Move formulas and cleanup ---
            self.play(FadeOut(nth_deriv_eval)) # Remove evaluated derivative
            self.taylor_formula_display = taylor_gen_formula # Store handle to the final T(x) formula Mobject
            self.play(self.taylor_formula_display.animate.scale(0.8).to_corner(UR))
            self.wait()

            # --- Approximation Visualization ---
            max_terms = 25 if center_a >= 2 else 15 # Use more terms for larger 'a'

            # Dot at center 'a'
            try:
                log_a_val = math.log(center_a)
            except ValueError:
                log_a_val = -1000 # Place dot off-screen if center_a <= 0
            
            self.dot_a = Dot(self.axes.c2p(center_a, log_a_val), color=YELLOW)
            self.play(Create(self.dot_a))
            self.wait(0.5)

            # Term counter setup
            self.term_counter = MathTex("N=0").scale(0.7).next_to(self.taylor_formula_display, DOWN, buff=0.2, aligned_edge=RIGHT)

            # Initial graph (N=0) - use try-except for robustness
            try:
                initial_approx_func = lambda x: taylorseries_log(x, 0, a=center_a)
                # Check if the function returns valid numbers before plotting
                test_y = initial_approx_func(center_a + 0.1) 
                if not isinstance(test_y, (int, float)) or math.isnan(test_y) or math.isinf(test_y):
                     raise ValueError("taylorseries_log returned invalid value")
                
                self.approx_graph = self.axes.plot(
                    initial_approx_func, 
                    x_range=[max(0.01, center_a - center_a - 0.5), min(4.5, center_a + center_a + 0.5)], # Dynamic x_range based on expected convergence
                    color=ORANGE,
                    use_smoothing=False # May help with sharp turns/divergence
                )
                
                self.play(
                    Create(self.approx_graph),
                    Write(self.term_counter),
                    self.taylor_formula_display[0][:4].animate.set_color(ORANGE), # Color T(x)=
                )
            except (ValueError, TypeError) as e:
                 print(f"Error plotting N=0 approximation for a={center_a}: {e}")
                 # Don't create graph, maybe show error text?
                 error_text = Tex("Plotting Error", color=RED).scale(0.5).move_to(self.axes.c2p(center_a, 0))
                 self.play(Write(error_text)) # Show error briefly
                 self.wait(1)
                 self.play(FadeOut(error_text))
                 # Set approx_graph to empty so cleanup doesn't fail
                 self.approx_graph = VMobject() 
                 
            self.wait(0.5)

            # Animate terms
            for i in range(1, max_terms + 1):
                new_term_counter = MathTex(f"N={i}").scale(0.7).move_to(self.term_counter)
                try:
                    approx_func = lambda x: taylorseries_log(x, i, a=center_a)
                    # Optional: Check validity like for N=0
                    test_y = approx_func(center_a + 0.1) 
                    if not isinstance(test_y, (int, float)) or math.isnan(test_y) or math.isinf(test_y):
                         raise ValueError("taylorseries_log returned invalid value")

                    new_graph = self.axes.plot(
                        approx_func, 
                         x_range=[max(0.01, center_a - center_a - 0.5), min(4.5, center_a + center_a + 0.5)], 
                        color=ORANGE,
                        use_smoothing=False
                    )

                    # Only play transform if self.approx_graph exists and has points
                    if self.approx_graph and self.approx_graph.has_points():
                         self.play(
                            Transform(self.approx_graph, new_graph),
                            Transform(self.term_counter, new_term_counter),
                            run_time=0.4 # Faster updates
                         )
                    else: # If initial plot failed, just create the new graph
                         self.approx_graph = new_graph
                         self.play(
                              Create(self.approx_graph),
                              Transform(self.term_counter, new_term_counter),
                              run_time=0.4
                         )
                         
                except (ValueError, TypeError) as e:
                     print(f"Error plotting N={i} approximation for a={center_a}: {e}")
                     # Stop animation for this center if plotting fails
                     break 
                     
                self.wait(0.05 if i > 5 else 0.15) # Shorter pauses

            self.wait(1)

            # --- Show Interval and Radius ---
            interval_start = 0 # Singularity
            interval_end = 2 * center_a
            radius = center_a

            # Visually clamp interval end to axes range if necessary
            plot_interval_end = min(interval_end, self.axes.x_range[1])
            plot_interval_start = max(interval_start, self.axes.x_range[0]) + 0.01 # Keep slightly off axis

            # Interval Brace
            if plot_interval_end > plot_interval_start: # Ensure valid points for brace
                interval_brace_obj = BraceBetweenPoints(self.axes.c2p(plot_interval_start, 0), self.axes.c2p(plot_interval_end, 0), direction=UP, color=RED)
                interval_text_obj = interval_brace_obj.get_text(f"Converges on ({interval_start}, {interval_end})").scale(0.6)
                self.play(GrowFromCenter(interval_brace_obj), Write(interval_text_obj))
                self.convergence_elements.add(interval_brace_obj, interval_text_obj) # Add to group for cleanup
            else:
                print(f"Warning: Cannot draw interval brace for a={center_a}")
            self.wait(0.5)

            # Radius Brace (from 'a' to interval_end)
            if plot_interval_end > center_a: # Ensure valid points
                radius_brace_obj = BraceBetweenPoints(self.axes.c2p(center_a, 0), self.axes.c2p(plot_interval_end, 0), direction=DOWN, color=YELLOW)
                radius_text_obj = radius_brace_obj.get_text(f"Radius R = {radius}").scale(0.6)
                self.play(GrowFromCenter(radius_brace_obj), Write(radius_text_obj))
                self.convergence_elements.add(radius_brace_obj, radius_text_obj) # Add to group
            else:
                 print(f"Warning: Cannot draw radius brace for a={center_a}")

            self.wait(2)


        def show_general_radius():
             # --- Cleanup from previous center (e.g., a=2) ---
            cleanup_targets = [self.approx_graph, self.taylor_formula_display, self.dot_a, self.term_counter]
            if self.convergence_elements and len(self.convergence_elements) > 0:
                 cleanup_targets.append(self.convergence_elements)
            objects_to_fade = [m for m in cleanup_targets if m and m.has_points()]
            if objects_to_fade:
                self.play(*[FadeOut(m) for m in objects_to_fade])
            # Also fade the specific f^(n)(x) formula, leaving axes and log graph
            self.play(FadeOut(self.nth_deriv_formula_display), FadeOut(self.log_label))
            self.wait()

            # --- General Case Visualization ---
            title = Tex("General Case: Radius of Convergence for $f(x)=\ln(x)$", font_size=36).to_edge(UP)
            self.play(Write(title))

            # Singularity at x=0
            singularity_pt = self.axes.c2p(0, 0)
            singularity_line = DashedLine(
                self.axes.c2p(0, self.axes.y_range[0]),
                self.axes.c2p(0, self.axes.y_range[1]),
                color=RED, stroke_width=3
            )
            singularity_label = Tex("Singularity!", color=RED, font_size=28).next_to(self.axes.c2p(0, 1.5), RIGHT, buff=0.1)
            self.play(Create(singularity_line), Write(singularity_label))
            self.wait(1)

            # General center 'a'
            a_val = ValueTracker(1.5)
            a_dot = Dot(color=YELLOW, radius=0.08)
            a_label = MathTex("a", color=YELLOW).scale(0.8)
            a_dot.add_updater(lambda m: m.move_to(self.axes.c2p(a_val.get_value(), 0)))
            a_label.add_updater(lambda m: m.next_to(a_dot, DOWN, buff=0.15))

            # Radius line, brace, text (with updaters)
            radius_line = Line(color=YELLOW, stroke_width=5)
            radius_brace = Brace(radius_line, direction=DOWN, color=YELLOW) # Temp init
            radius_text = MathTex("R = a", color=YELLOW).scale(0.7)
            radius_line.add_updater(lambda m: m.put_start_and_end_on(self.axes.c2p(a_val.get_value(), 0), singularity_pt))
            def radius_updater(mob):
                # Check if line has valid length before creating brace
                if radius_line.get_length() > 1e-3:
                    mob.become(Brace(radius_line, direction=DOWN, color=YELLOW))
                    radius_text.next_to(mob, DOWN, buff=0.1)
                else:
                     mob.become(VMobject()) # Make brace empty if line is too short
                     radius_text.become(VMobject())
            radius_brace.add_updater(radius_updater)
            radius_text.add_updater(lambda m: m.next_to(radius_brace, DOWN, buff=0.1) if radius_brace.has_points() else m.become(VMobject()))

            # Interval brace, text (with updaters)
            interval_brace = VMobject() # Init empty
            interval_text = MathTex("(0, 2a)", color=BLUE).scale(0.7)
            def interval_updater(mob):
                current_a = a_val.get_value()
                end_x = min(2*current_a, self.axes.x_range[1])
                start_x = max(1e-3, self.axes.x_range[0]) # Avoid 0 and negative start
                if end_x > start_x:
                     # Use BraceBetweenPoints for axis alignment
                     mob.become(BraceBetweenPoints(self.axes.c2p(start_x, 0), self.axes.c2p(end_x, 0), direction=UP, color=BLUE))
                     interval_text.next_to(mob, UP, buff=0.1)
                     # Dynamically update text
                     interval_text_val = MathTex(f"(0, {2*current_a:.1f})", color=BLUE).scale(0.7).next_to(mob, UP, buff=0.1)
                     interval_text.become(interval_text_val)
                else:
                    mob.become(VMobject())
                    interval_text.become(VMobject())
            interval_brace.add_updater(interval_updater)
            interval_text.add_updater(lambda m: m.next_to(interval_brace, UP, buff=0.1) if interval_brace.has_points() else m.become(VMobject()))

            # Initial creation
            self.play(Create(a_dot), Write(a_label))
            self.play(Create(radius_line))
            # Need to manually call updater once before playing creation animation
            radius_brace.update()
            interval_brace.update()
            self.play(GrowFromCenter(radius_brace), Write(radius_text))
            self.play(GrowFromCenter(interval_brace), Write(interval_text))
            self.wait(1)

            # Animate 'a' changing
            explanation_text = Tex(
                "The distance from center 'a' to the singularity at $x=0$ determines the radius $R=a$.",
                font_size=28
            ).next_to(title, DOWN, buff=0.3)
            self.play(Write(explanation_text))
            self.wait(1)

            self.play(a_val.animate.set_value(1), run_time=2)
            self.wait(1)
            self.play(a_val.animate.set_value(2.1), run_time=2) # Go slightly beyond 2
            self.wait(1)
            self.play(a_val.animate.set_value(0.5), run_time=2)
            self.wait(1)
            self.play(a_val.animate.set_value(1.5), run_time=1) # Return to generic
            self.wait(2)

            # Final Conclusion Text
            conclusion = Tex(
                r"The Taylor series for $\ln(x)$ centered at $a>0$ converges on $(0, 2a)$ with radius $R=a$.",
                font_size=32
            ).to_edge(DOWN, buff=0.5)
            self.play(Write(conclusion))
            self.wait(3)

            # Cleanup updaters before finishing
            # ... (clear_updaters calls as before) ...
            a_dot.clear_updaters()
            a_label.clear_updaters()
            radius_line.clear_updaters()
            radius_brace.clear_updaters()
            radius_text.clear_updaters()
            interval_brace.clear_updaters()
            interval_text.clear_updaters()

            # Fade out general explanation elements
            self.play(FadeOut(title, singularity_line, singularity_label, a_dot, a_label, radius_line, radius_brace, radius_text, interval_brace, interval_text, explanation_text, conclusion))
            self.wait(1)


        # --- Call the functions in order ---
        setup_graph()
        derive_nth_derivative()
        show_taylor_for_center(center_a=1)
        show_taylor_for_center(center_a=2)
        show_general_radius()

        self.wait(2) # Hold final axes and log graph

class ComplexRadiusOfConvergence_v2(ThreeDScene): # Use ThreeDScene
    # --- Helper for 3D Surface ---
    def func_3d_abs_1_over_1pz2(self, x, y):
        z = complex(x, y)
        denominator = 1 + z**2
        # Add epsilon to avoid division by zero exactly at poles
        if abs(denominator) < 1e-6:
            return 5 # Return a large, but not infinite, value
        val = abs(1 / denominator)
        # Cap height for visualization
        return min(val, 5) 
    
    # --- Helper Function for Taylor Approximation ---
    def f_deriv(self, x_val, n):
        x = sympy.symbols('x')
        f = 1 / (1 + x**2)
        f_n = f
        for _ in range(n):
            f_n = sympy.diff(f_n, x)
        return float(f_n.subs(x, x_val))

    # --- Modify taylor_approx_at_a ---
    def taylor_approx_at_a(self, x, a, n_terms):
        """Calculates the Taylor expansion of 1/(1+x^2) around 'a' up to n_terms."""
        val = 0.0
        a = float(a) # Ensure 'a' is a float
        x = float(x) # Ensure 'x' is a float
        for n in range(n_terms + 1):
            deriv_at_a = self.f_deriv(a, n)
            term = deriv_at_a / math.factorial(n) * (x - a)**n
            # Cap term magnitude to avoid excessive spikes when diverging
            if abs(term) > 100: # Adjust cap as needed
                term = np.sign(term) * 100
            val += term
                
        # Cap the output value
        if abs(val) > 5: # Limit based on axes range
            return np.sign(val) * 5
        return val
    
    def construct(self):

        # Keep N_TAYLOR_TERMS low if using Sympy! Performance depends heavily on this.
        N_TAYLOR_TERMS = 31 # Using 4 terms as per example taylor_approx_at_a

        # --- Part 0: Initial Setup ---
        main_axes = Axes(
            x_range=[-4.5, 4.5, 1], y_range=[-0.5, 2.0, 0.5],
            x_length=12, y_length=5,
            axis_config={"include_numbers": True}
        ).to_edge(DOWN, buff=0.75)
        main_axes_labels = main_axes.get_axis_labels(x_label="x", y_label="f(x)")

        func = lambda x: 1 / (1 + x**2)
        func_graph = main_axes.plot(func, color=BLUE, x_range=[-4.5, 4.5])

        func_label = MathTex(r"f(x) = \frac{1}{1+x^2}", color=BLUE).to_corner(UR).set_z_index(10)
        self.add_fixed_in_frame_mobjects(func_label)

        approx_graph_dynamic = VMobject().set_z_index(1)
        # **** OPTIMIZATION: Store last 'a' value on the mobject itself ****
        approx_graph_dynamic._last_a_value = None # Initialize

        self.play(
            Create(main_axes), Write(main_axes_labels),
            Create(func_graph),
            run_time=1
        )
        self.wait()

        # --- Part 1: Show ROC & Approximation for a=0 ---
        center_a_val = ValueTracker(0.0)
        center_a_dot_on_graph = Dot(color=YELLOW, radius=0.08).set_z_index(2)
        vertical_line = DashedLine(stroke_width=2, color=YELLOW, stroke_opacity=0.7)
        radius_func = lambda a: np.sqrt(a**2 + 1) # Distance from a to +/- i
        roc_group = VGroup().set_z_index(2) # For brace on x-axis

        # --- Updater for Moving Dot and Line ---
        def dot_line_updater(mob):
             a = center_a_val.get_value()
             # Use try-except for safety, although func(a) is well-behaved here
             try: y_val = func(a)
             except Exception: y_val = 0 # Default to 0 on error
             if not np.isfinite(y_val): y_val = 0 # Handle potential inf/nan
             graph_point = main_axes.c2p(a, y_val)
             center_a_dot_on_graph.move_to(graph_point)
             vertical_line.put_start_and_end_on(graph_point, main_axes.c2p(a, 0))
        # Use a dummy mobject for the updater so it can be added/removed easily
        dummy_updater_mob = Mobject().add_updater(dot_line_updater)
        self.add(dummy_updater_mob) # Add the updater immediately

        # --- OPTIMIZED Updater for Dynamic Approximation Graph ---
        def approx_graph_updater(mob):
             current_a = center_a_val.get_value()
             previous_a = getattr(mob, '_last_a_value', None) # Get previous value

             tolerance = 1e-9 # Tolerance for float comparison

             # **** Check if 'a' has changed significantly ****
             a_has_changed = (previous_a is None) or (abs(current_a - previous_a) > tolerance)

             if a_has_changed:
                  # --- Perform expensive calculation ONLY if 'a' changed ---
                  # print(f"Recalculating graph for a = {current_a}") # Debug output
                  a = current_a # Use current_a for clarity below
                  R = radius_func(a)
                  # Define plot range based on ROC, but clamp to axes limits
                  plot_start = max(a - R - 0.2, main_axes.x_range[0])
                  plot_end = min(a + R + 0.2, main_axes.x_range[1])

                  new_graph_generated = False # Flag to check if graph was made
                  # Ensure plot range is valid
                  if plot_end > plot_start + 0.05: # Need some interval width
                       current_approx_func = lambda x: self.taylor_approx_at_a(x, a, N_TAYLOR_TERMS)
                       # Generate x values within the calculated range
                       x_values = np.linspace(plot_start, plot_end, num=150) # Increased points for smoothness
                       y_values = np.array([current_approx_func(x) for x in x_values])

                       # Filter out non-finite values before plotting
                       valid_indices = np.isfinite(y_values) & (np.abs(y_values) < 10) # Also filter extreme values
                       x_values = x_values[valid_indices]
                       y_values = y_values[valid_indices]

                       # Only plot if we have at least two valid points
                       if len(x_values) > 1:
                            new_graph = main_axes.plot_line_graph(
                                x_values=x_values, y_values=y_values,
                                line_color=ORANGE, stroke_width=3.5,
                                add_vertex_dots=False # Usually false for smooth plots
                            )
                            mob.become(new_graph) # Use become to smoothly update
                            new_graph_generated = True # Mark as successful

                  # If plot range was invalid OR graph generation failed, show an empty graph
                  if not new_graph_generated:
                       mob.become(VMobject()) # Become empty

                  # --- Store the current 'a' value for the next frame ---
                  mob._last_a_value = current_a
             # else: # 'a' hasn't changed, do nothing, mob keeps its previous state
                  # print(f"Skipping graph recalc for a = {current_a}") # Debug output
                  pass

        approx_graph_dynamic.add_updater(approx_graph_updater)

        # --- Updater for ROC Brace (on x-axis) ---
        def roc_brace_updater(mob):
            a = center_a_val.get_value()
            R = radius_func(a)
            start_x = a - R; end_x = a + R
            # Clamp the brace ends to the visible x-axis range
            start_x_clamped = max(start_x, main_axes.x_range[0])
            end_x_clamped = min(end_x, main_axes.x_range[1])

            new_group = VGroup() # Start with an empty group
            # Only create brace if the clamped interval is valid
            if end_x_clamped > start_x_clamped + 0.01:
                # Use BraceBetweenPoints for precision
                new_brace = BraceBetweenPoints(
                    main_axes.c2p(start_x_clamped, 0),
                    main_axes.c2p(end_x_clamped, 0),
                    direction=DOWN, color=RED
                )
                new_text = Tex(f"R = {R:.2f}", font_size=28).next_to(new_brace, DOWN, buff=0.1)
                # Add background for better readability
                bg = BackgroundRectangle(new_text, color=config.background_color, fill_opacity=0.8, buff=0.05)
                new_group.add(bg, new_text, new_brace) # Add brace last so text bg is behind brace tip if needed
            mob.become(new_group) # Update the VGroup content

        roc_group.add_updater(roc_brace_updater)

        # Initial display for a=0
        # Force initial calculation by calling update(0) for each updater
        dummy_updater_mob.update(0)
        approx_graph_dynamic.update(0)
        roc_group.update(0)

        self.play(
            Create(center_a_dot_on_graph), Create(vertical_line),
            Create(approx_graph_dynamic), Create(roc_group), # Use Create for initial appearance
            run_time=1
        )
        self.wait(1)

        puzzle_text = Tex("Approximation (orange) matches near 'a', limited by R", font_size=30).next_to(roc_group, DOWN, buff=0.3)
        self.play(Write(puzzle_text))
        self.wait(2)
        self.play(FadeOut(puzzle_text))
        self.wait(0.5)

        # --- Part 2: Dynamic ROC (Real Axis View) ---
        dynamic_explanation = Tex("Observe how approximation and ROC change with 'a'", font_size=30).to_edge(UP)
        self.add_fixed_in_frame_mobjects(dynamic_explanation)
        self.play(Write(dynamic_explanation))
        self.wait(1)

        # Animate 'a' changing. Updaters handle the rest smoothly.
        self.play(center_a_val.animate.set_value(-2), run_time=3, rate_func=smooth)
        self.wait(0.5) # Pause - graph should NOT recalculate here if a hasn't changed
        self.play(center_a_val.animate.set_value(2), run_time=4, rate_func=smooth)
        self.wait(1) # Pause - graph should NOT recalculate here

        # --- Clear updaters before transition ---
        self.remove(dummy_updater_mob) # Remove the dummy object holding the dot/line updater
        approx_graph_dynamic.clear_updaters()
        roc_group.clear_updaters()

        self.play(FadeOut(dynamic_explanation))
        self.remove_fixed_in_frame_mobjects(dynamic_explanation)
        self.wait(0.5)

        # --- Part 3 & 4: 3D Reveal ---
        reveal_text = Tex("The reason lies in the complex plane!", font_size=36).to_edge(UP)
        self.add_fixed_in_frame_mobjects(reveal_text)
        self.play(Write(reveal_text))
        self.wait(1)

        # Fade out 2D elements
        fade_out_2d = [
            main_axes, main_axes_labels, func_graph, approx_graph_dynamic,
            center_a_dot_on_graph, vertical_line, roc_group
        ]
        # Filter out None just in case, though shouldn't be necessary here
        self.play(*[FadeOut(m) for m in fade_out_2d if m is not None],
                  FadeOut(reveal_text))
        self.remove_fixed_in_frame_mobjects(reveal_text) # Remove after fade out
        self.wait(0.5)

        # --- 3D Axes, Surface, Poles ---
        axes_3d = ThreeDAxes(
            x_range=[-2.5, 2.5, 1], y_range=[-2.5, 2.5, 1], z_range=[0, 5.5, 1],
            x_length=7, y_length=7, z_length=4,
        )
        label_re = Tex("Re(z)", font_size=24).move_to(axes_3d.x_axis.get_end() + 0.4*RIGHT)
        label_im = Tex("Im(z)", font_size=24).move_to(axes_3d.z_axis.get_end() + 0.4*OUT)
        label_abs = Tex("$|f(z)|$", font_size=24).move_to(axes_3d.y_axis.get_top() + 0.4*UP)
        self.add_fixed_in_frame_mobjects(label_re)
        self.add_fixed_in_frame_mobjects(label_im)
        self.add_fixed_in_frame_mobjects(label_abs)
        labels_3d_group = VGroup(label_re, label_im, label_abs)

        surface = axes_3d.plot_surface(
            lambda u, v: self.func_3d_abs_1_over_1pz2(u, v), u_range=[-2.5, 2.5], v_range=[-2.5, 2.5],
            resolution=(48, 48), colorscale=[(BLUE, 0), (GREEN, 0.5), (YELLOW, 1.5), (RED, 3)], fill_opacity=0.8
        )
        pole_pos_i = axes_3d.c2p(0, 1, 0); pole_neg_i = axes_3d.c2p(0, -1, 0)
        pole_marker_pos = Dot3D(point=pole_pos_i, color=RED, radius=0.1)
        pole_marker_neg = Dot3D(point=pole_neg_i, color=RED, radius=0.1)
        pole_label_pos = MathTex("+i", color=RED, font_size=30).move_to(pole_marker_pos.get_center() + 0.4*(OUT+RIGHT*0.5+UP*0.5))
        pole_label_neg = MathTex("-i", color=RED, font_size=30).move_to(pole_marker_neg.get_center() + 0.4*(OUT+RIGHT*0.5+DOWN*0.5))
        poles_group = VGroup(pole_marker_pos, pole_marker_neg, pole_label_pos, pole_label_neg)

        self.set_camera_orientation(phi=70 * DEGREES, theta=-110 * DEGREES)
        self.play(Create(axes_3d)); self.play(Write(labels_3d_group)) # Create separately
        self.play(Create(surface), FadeIn(poles_group, scale=0.5), run_time=3)
        singularity_text = Tex("Surface shows singularities at $z = \pm i$", font_size=30).to_corner(UL)
        self.add_fixed_in_frame_mobjects(singularity_text)
        self.play(Write(singularity_text)); self.wait(2)
        self.move_camera(theta=70 * DEGREES, phi=60*DEGREES, run_time=4); self.wait(2)


        # --- Part 5: Return to 2D + Complex Plane View ---
        return_text = Tex("Back to the real axis view...", font_size=30).move_to(singularity_text)
        self.add_fixed_in_frame_mobjects(return_text)

        # *** IMPORTANT: Clear 3D billboard updaters ***
        for label in labels_3d_group: label.clear_updaters()
        pole_label_pos.clear_updaters()
        pole_label_neg.clear_updaters()

        self.play(
            FadeOut(axes_3d), FadeOut(labels_3d_group), FadeOut(surface), FadeOut(poles_group),
            ReplacementTransform(singularity_text, return_text)
        )
        self.wait(1)
        self.play(FadeOut(return_text)) # Fade it out properly
        self.remove_fixed_in_frame_mobjects(singularity_text) # remove old text
        self.remove_fixed_in_frame_mobjects(return_text) # remove new text after it fades

        # Reset camera for 2D view
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES)

        # --- Prepare 2D elements for reappearance ---
        center_a_val.set_value(0) # Reset 'a' value
        # *** ISSUE 2 FIX: Force updaters to run *before* FadeIn ***
        # 1. Re-add updaters
        self.add(dummy_updater_mob) # Handles dot and line
        approx_graph_dynamic._last_a_value = None # Force recalc
        approx_graph_dynamic.add_updater(approx_graph_updater)
        roc_group.add_updater(roc_brace_updater)
        # 2. Force update calculation while elements are still invisible
        dummy_updater_mob.update(0)
        approx_graph_dynamic.update(0) # Calculates graph for a=0
        roc_group.update(0) # Calculates brace for a=0

        # Now FadeIn the elements - they will appear in the correct a=0 state
        self.play(
            FadeIn(main_axes), FadeIn(main_axes_labels), FadeIn(func_graph),
            FadeIn(center_a_dot_on_graph), FadeIn(vertical_line),
            FadeIn(approx_graph_dynamic), # Fades in the pre-calculated a=0 graph
            # FadeIn(roc_group) # We will fade this in later explicitly
            run_time=1.5
        )
        self.wait(0.5)

        # --- Create Complex Plane Subplot (Top Left) ---
        complex_plane = ComplexPlane(
             x_range=[-2.2, 2.2, 1], y_range=[-2.2, 2.2, 1],
             x_length=3.5, y_length=3.5, # Slightly larger
             background_line_style={"stroke_opacity": 0.3, "stroke_width": 1.5}
         ).scale(0.8).to_corner(UL, buff=0.2) # Added buffer

        cp_labels = VGroup(
            Tex("Re",font_size=20).next_to(complex_plane.x_axis,DR,buff=0.1),
            Tex("Im",font_size=20).next_to(complex_plane.y_axis,UR,buff=0.1)
        )
        # Poles at +i (0,1) and -i (0,-1) in complex plane
        pole_cp_pos_pt = complex_plane.n2p(1j)
        pole_cp_neg_pt = complex_plane.n2p(-1j)
        pole_cp_pos = Dot(pole_cp_pos_pt, color=RED, radius=0.05)
        pole_cp_neg = Dot(pole_cp_neg_pt, color=RED, radius=0.05)
        pole_cp_label_pos = MathTex("+i", color=RED, font_size=20).next_to(pole_cp_pos, UR, buff=0.05)
        pole_cp_label_neg = MathTex("-i", color=RED, font_size=20).next_to(pole_cp_neg, DR, buff=0.05)
        cp_poles_group = VGroup(pole_cp_pos, pole_cp_neg, pole_cp_label_pos, pole_cp_label_neg)

        # Dot representing 'a' on the real axis of the complex plane
        a_dot_cp = Dot(color=YELLOW, radius=0.05).set_z_index(1)
        a_dot_cp.add_updater(lambda m: m.move_to(complex_plane.n2p(complex(center_a_val.get_value(), 0))))
        a_label_cp = MathTex("a", color=YELLOW, font_size=20)
        a_label_cp.add_updater(lambda m: m.next_to(a_dot_cp, DOWN, buff=0.1))

        # Line from 'a' to nearest singularity (let's choose +i)
        dist_line = Line(color=YELLOW, stroke_width=2, stroke_opacity=0.8).set_z_index(0)
        dist_line.add_updater(lambda m: m.put_start_and_end_on(
            a_dot_cp.get_center(), # Use dot's current center
            pole_cp_pos_pt # Fixed point for +i
        ))

        # Updater for Distance Brace/Text in Complex Plane
        dist_display_group_cp = VGroup().set_z_index(2) # Ensure it's on top
        def dist_updater_cp(mob):
            a = center_a_val.get_value()
            R = radius_func(a) # This is sqrt(a^2 + 1)
            start_pt = dist_line.get_start()
            end_pt = dist_line.get_end()
            new_group = VGroup()
            # Only draw if line has significant length
            if np.linalg.norm(end_pt - start_pt) > 0.02:
                 line_vec = end_pt - start_pt
                 # Calculate perpendicular vector pointing away from origin (usually)
                 perp_vec = normalize(np.array([-line_vec[1], line_vec[0], 0]))
                 mid_point = dist_line.get_center()
                 origin_vec = mid_point - complex_plane.get_origin()
                 # Ensure brace points outwards from origin if origin is not between start/end
                 if abs(np.linalg.norm(origin_vec)) > 1e-6 and np.dot(perp_vec, origin_vec) < 0:
                     perp_vec *= -1
                 # Create brace along the line
                 new_brace = Brace(dist_line, direction=perp_vec, color=YELLOW, sharpness=0.7, buff=0.05)
                 new_text = Tex(f"R = {R:.2f}", font_size=24).next_to(new_brace, perp_vec, buff=0.05) # Smaller font
                 bg = BackgroundRectangle(new_text, color=config.background_color, fill_opacity=0.8, buff=0.05)
                 new_group.add(bg, new_text, new_brace) # Brace last
            mob.become(new_group)

        dist_display_group_cp.add_updater(dist_updater_cp)

        # --- Animate creation of subplot elements ---
        # Add updaters *before* animating creation
        a_dot_cp.update(0)
        a_label_cp.update(0)
        dist_line.update(0)
        dist_display_group_cp.update(0) # Calculate initial state

        self.play(
            FadeIn(complex_plane), Write(cp_labels), FadeIn(cp_poles_group),
            FadeIn(a_dot_cp), Write(a_label_cp), FadeIn(dist_line),
            # *** ISSUE 3 FIX: Use Create or Write for the group ***
            run_time=1.5
        )
        self.play(FadeIn(dist_display_group_cp))
        self.wait(1)

        # Display main ROC brace again
        # It was updated off-screen before, now just FadeIn
        # *** ISSUE 4 FIX: Use FadeIn without self.add beforehand ***
        self.play(FadeIn(roc_group))
        self.wait(1)

        # Run the animation again, with complex plane visualization
        final_explanation = Tex("ROC = Distance from 'a' to nearest singularity $(\pm i)$", font_size=30).to_edge(UP)
        self.add_fixed_in_frame_mobjects(final_explanation)
        self.play(Write(final_explanation))
        self.wait(0.5)

        self.play(center_a_val.animate.set_value(-2), run_time=3, rate_func=smooth)
        self.wait(0.5) # Pause
        self.play(center_a_val.animate.set_value(2), run_time=4, rate_func=smooth)
        self.wait(2) # Pause

        # --- Cleanup updaters before final slide ---
        self.remove(dummy_updater_mob)
        approx_graph_dynamic.clear_updaters()
        roc_group.clear_updaters()
        a_dot_cp.clear_updaters()
        a_label_cp.clear_updaters()
        dist_line.clear_updaters()
        dist_display_group_cp.clear_updaters()
        # Note: 3D billboard updaters were already cleared

        self.wait(1)

        # --- Final Conclusion Slide ---
        # Group all elements currently on screen to fade them out
        elements_to_fade = VGroup(
            main_axes, main_axes_labels, func_graph, center_a_dot_on_graph, vertical_line,
            complex_plane, cp_labels, cp_poles_group, a_dot_cp, a_label_cp, dist_line,
            roc_group, dist_display_group_cp, approx_graph_dynamic
        )
        # Manim handles fading out VGroups containing other mobjects
        self.play(
            FadeOut(elements_to_fade),
            FadeOut(final_explanation),
            FadeOut(func_label) # Fade out fixed mobjects
        )
        # Remove fixed mobjects after they are faded
        self.remove_fixed_in_frame_mobjects(final_explanation, func_label)
        self.wait(1)

        # Conclusion Text
        conclusion_line1 = Tex("The Radius of Convergence (ROC) of a Taylor series")
        conclusion_line2 = Tex(r"centered at '$a$' is the distance from '$a$' to the")
        conclusion_line3 = Tex(r"\textbf{nearest singularity} of the function")
        conclusion_line4 = Tex(r"in the \textbf{complex plane}.")
        conclusion_group = VGroup(conclusion_line1, conclusion_line2, conclusion_line3, conclusion_line4).arrange(DOWN, buff=0.3).scale(0.9)

        caveat_text = Tex(r"*Applies to functions analytic around '$a$'. If no finite singularities exist (entire functions), ROC = $\infty$.", font_size=24, color=GREY_B).to_edge(DOWN, buff=0.3)

        self.play(Write(conclusion_group))
        self.wait(1.5)
        self.play(FadeIn(caveat_text, shift=UP*0.2))
        self.wait(8)

class Origin_Radius(ThreeDScene):
    '''
    def construct(self):
        # Setup 3D axes
        axes = ThreeDAxes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            z_range=[0, 1, 0.2],
            x_length=7,
            y_length=7,
            z_length=5
        )

        # Function for plotting 2D graph along the xz-plane
        def func_2d(x):
            return 1 / (x**2 + 1)

        # Convert 2D function to 3D by ignoring y-component
        graph_2d = axes.plot_line_graph(
            x_values=np.linspace(-2, 2, 100),
            y_values=[func_2d(x) for x in np.linspace(-2, 2, 100)],
            line_color=GREEN,
            add_vertex_dots=False,
        )

        # Define the 3D function for complex input z
        def func_3d(x, y):
            z = complex(x, y)
            # Assuming we want to visualize the function for all z
            return np.real(1 / (z**2 + 1))

        # Create the 3D surface plot
        surface = Surface(
            lambda u, v: axes.c2p(u, v, func_3d(u, v)),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(30, 30),
            fill_opacity=0.5,  # Semi-transparent
            stroke_opacity=0.5,
        )

        # Start with the camera positioned to show only the xz-plane
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES)
        self.add(axes, graph_2d)

        ## Move the camera to reveal the 3D nature and the y-axis
        self.move_camera(phi=70 * DEGREES, theta=-45 * DEGREES)
        self.wait()

        # Transition from 2D graph to 3D surface
        self.play(Transform(graph_2d, surface), run_time=3)
        self.wait(3)

    '''
    def construct(self):
        axes = ThreeDAxes(
            x_range=[-2, 2, 0.5],
            y_range=[-2, 2, 0.5],
            z_range=[-2, 2, 0.5],
            x_length=7,
            y_length=7,
            z_length=5
        )
        x_label = axes.get_x_axis_label("y").set_color(WHITE)
        y_label = axes.get_y_axis_label("x").set_color(WHITE)
        z_label = MathTex(r"\Re\{f(x,z)\}").next_to(axes.z_axis.get_end()).set_color(WHITE)

        def func_r(x):
            '''returns z-axis value for x-axis input'''
            result = 1/(x**2 + 1)
            return result
        
        # Define the function to plot
        # This function takes two real arguments, x and y, and returns the real part of 1 / (z^2 + 1)
        def func(x, z):
            '''returns the real part of 1 / (z^2 + 1) on y axis for complex input y = x + iz'''
            y = complex(x, z)
            try:
                result = 1 / (y**2 + 1)
            except:
                result = 3
            return np.real(result) if np.real(result) < 3 else 3
        
        # plot grapg_r with x input on the z axis as output, not the y axis
        graph_r = ParametricFunction(
                    lambda t: axes.c2p(0, t, func_r(t)), # Convert to 3D points
                    t_range=[-2, 2],
                    color=BLUE
                )

        # Create a parametric function plot of the function
        # This surface uses the input from the x and z axis to the y axis
        """ graph = ParametricFunction(
            lambda u, v: axes.c2p(v, u, func(u, v)), # Convert to 3D points
            u_range=[-2, 2],
            v_range=[-2, 2],
            color=BLUE
        ) """

        graph = Surface(
            lambda u, v: axes.c2p(v, u, func(u, v)),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(150, 150),
            fill_opacity=0.5,
        )

        annotations = [
            Text("i", font_size=24).move_to(axes.c2p(1, 0, 0)).add_background_rectangle(),
            Text("-i", font_size=24).move_to(axes.c2p(-1, 0, 0)).add_background_rectangle(),
            Text("1", font_size=24).move_to(axes.c2p(0, 1, 0.1)).add_background_rectangle(),
            Text("-1", font_size=24).move_to(axes.c2p(0, -1, 0.1)).add_background_rectangle(),
            Text("1", font_size=24).move_to(axes.c2p(-0.1, 0, 1)).add_background_rectangle(),
            Text("-1", font_size=24).move_to(axes.c2p(-0.1, 0, -1)).add_background_rectangle()
        ]

        # Styling the graph
        graph.set_style(stroke_width=1, stroke_color=WHITE)
        graph.set_fill_by_value(axes=axes, colors=[(BLUE_E, -0.5), (GREEN_E, 0.5), (YELLOW_E, 1.5)])

        # Add red lines for the poles
        poles = VGroup(
            Line(axes.c2p(1, 0, -3), axes.c2p(1, 0, 3), color=RED),
            Line(axes.c2p(-1, 0, -3), axes.c2p(-1, 0, 3), color=RED)
        )

        # Adding axes and graph to the scene
        self.set_camera_orientation(phi=90 * DEGREES, theta=0 * DEGREES)
        self.play(Create(axes), Create(x_label), Create(y_label), Create(z_label), AnimationGroup(*[Create(annotation) for annotation in annotations[2:]]))
        self.wait()
        self.play(Create(graph_r))
        self.wait()
        self.move_camera(phi=60 * DEGREES, theta=45 * DEGREES)
        self.wait()
        self.play(AnimationGroup(*[Create(annotation) for annotation in annotations[:2]]))
        self.wait()
        self.play(Create(graph))
        self.wait()
        self.play(Create(poles))
        self.wait()
        def begin_camera_roation_around_y_2(self, rate: float = 0.02):
            """
            This method begins an ambient rotation of the camera about the Y_AXIS,
            in the anticlockwise direction

            Parameters
            ----------
            rate
                The rate at which the camera should rotate about the Y_AXIS.
                Negative rate means clockwise rotation.
            """
            # alpha_0 is arctan(tan(phi)/tan(theta))
            alpha_0 = np.arctan(np.tan(self.camera.phi_tracker.get_value())/np.tan(self.camera.theta_tracker.get_value()))
            # increase alpha_0 by rate and calculate new phi and theta
            def update_alpha(dt, alpha):
                # get x,y,z coordinates of camera
                x, y, z = self.camera.get_position()
                distance = np.sqrt(x**2 + y**2 + z**2)
                x_1_new = distance * np.sin(alpha + rate * dt)
                # y stays constant because we rotate around y
                z_1_new = distance * np.cos(alpha + rate * dt)
                # calculate new phi and theta
                theta_new = np.arccos(z_1_new/distance)
                # phi_new = sgn(x_1_new)*arccos(x_1_new/(x_1_new**2 + y**2))
                phi_new = np.sign(x_1_new)*np.arccos(x_1_new/(x_1_new**2 + y**2))
                # set new phi and theta
                self.camera.theta_tracker.set_value(theta_new)
                self.camera.phi_tracker.set_value(phi_new)
                # update camera position
                self.camera.set_position([x_1_new, y, z_1_new])
            vt = ValueTracker(alpha_0)
            self.camera.add_updater(lambda dt: update_alpha(dt, vt.get_value()))
            self.play(vt.animate.set_value(alpha_0 + np.pi))
        # Move the camere 360 degrees around the z axis
        self.begin_ambient_camera_rotation(rate=0.5)
        self.wait(15)
        self.stop_ambient_camera_rotation()
    
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
        g1 = axes.plot(lambda x: math.sin(x))
        #stretch_matrix = [[5,0],[0,1]]
        #self.play(ApplyMatrix(stretch_matrix, g1))
        #self.play(FadeOut(g1))
        self.wait()
        x_pos = [x*np.pi for x in range(-5, 6)]
        x_labels = [
            MathTex("-5\pi"),MathTex("-4\pi"),MathTex("-3\pi"), MathTex("-2\pi"), MathTex ("-\pi"), 
            MathTex("0"), 
            MathTex("\pi"), MathTex("2\pi"), MathTex("3\pi"), MathTex("4\pi"), MathTex("5\pi")
        ]
        x_dict = dict(zip(x_pos, x_labels))
        axes.add_coordinates(x_dict)

        self.play(FadeIn(axes), FadeIn(g1))
        #stretch_matrix = [[0.2,0],[0,1]]
        #self.play(Transform(axes, axes2), ApplyMatrix(stretch_matrix, g1))