"""Manim-Animiertes Video für die Taylorreihe einer Funktion"""

import math
#import functools
from manim import *


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
    
        approximation_term_parts = [MathTex("f(x) = ").set_color(GREEN).to_corner(UL), MathTex("1"), MathTex(r"-\frac{x^{2}}{2}"),
            MathTex(r"+\frac{x^{4}}{24}"), MathTex(r"-\frac{x^{6}}{720}"), MathTex(r"+\frac{x^{8}}{40320}"), MathTex(r"-\frac{x^{10}}{3628800}"),
            MathTex(r"+\frac{x^{12}}{479001600}"), MathTex(r"\cdots")]
        def show_cosine_approximation_n_to_m(start_degree, finish_degree):
            self.play(Write(approximation_term_parts[0]))
            for i in range(start_degree, finish_degree+1):
                if i == start_degree:
                    cos_appr = axes.plot(lambda x: taylorseries_cosine(x, i), color = GREEN)
                    approximation_term_parts[i+1].scale(0.8).next_to(approximation_term_parts[i]).set_color(GREEN)
                    self.play(Create(cos_appr), Write(approximation_term_parts[i+1]))
                    self.wait()
                else:
                    next_iteration = axes.plot(lambda x: taylorseries_cosine(x, i), color = GREEN)
                    if i < len(approximation_term_parts)-1:
                        approximation_term_parts[i+1].scale(0.8).next_to(approximation_term_parts[i]).set_color(GREEN)
                        self.play(Transform(cos_appr, next_iteration), Write(approximation_term_parts[i+1]))
                    else:
                        self.play(Transform(cos_appr, next_iteration))
                    self.wait()

        show_cosine_approximation_n_to_m(0,10)

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
            log_graph = axes.plot(lambda x: math.log(x), x_range=[0.01, 4.5, 0.01], color=BLUE)
            log_label = MathTex("f(x)=log(x)").set_color(BLUE).to_corner(UR).scale(0.8).shift(2*DOWN)
            self.play(FadeIn(axes))
            self.wait()
            self.play(Write(log_graph))
            self.play(Write(log_label))
            self.wait()
        
        def calculate_derivatives():
            text_scale = 0.85
            gap = 0.5
            function = MathTex("f(x)=log(x)").scale(text_scale).to_corner(UL)
            first_deriv = MathTex(r"f'(x)=\frac{1}{x}").scale(text_scale).next_to(function.get_corner(LEFT), direction=DOWN, aligned_edge=LEFT, buff = gap)
            second_deriv = MathTex(r"f''(x)=-\frac{1}{x^2}").scale(text_scale).next_to(first_deriv.get_corner(LEFT), direction=DOWN, aligned_edge=LEFT, buff = gap)
            third_deriv = MathTex(r"f'''(x)=\frac{1\cdot2}{x^3}").scale(text_scale).next_to(second_deriv.get_corner(LEFT), direction=DOWN, aligned_edge=LEFT, buff = gap)
            fourth_deriv = MathTex(r"f^{(4)}(x)=-\frac{1\cdot2\cdot3}{x^4}").scale(text_scale).next_to(third_deriv.get_corner(LEFT), direction=DOWN, aligned_edge=LEFT, buff = gap)
            result_arrow = Arrow(start=function.get_right(), end=function.get_right()+[2,0,0], color=RED, buff=0.1).scale(text_scale)
            nth_deriv_start = MathTex(r"f^{(n)}(x)=\cdots\frac{\cdots}{x^n}").scale(text_scale+0.1).next_to(result_arrow.get_corner(RIGHT), direction=RIGHT, buff = 0, aligned_edge=LEFT).shift(0.1*DOWN)
            
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

            self.play(Transform(nth_deriv_start[0][11:14], MathTex(r"(n-1)!").scale(text_scale+0.1).next_to(nth_deriv_start[0][11:14].get_corner(LEFT), direction=RIGHT, buff = 0, aligned_edge=LEFT)),
                    Transform(nth_deriv_start[0][14], MathTex(r"\frac{(n-1)!}{x^n}")[0][6].scale(text_scale+0.1).next_to(nth_deriv_start[0][14].get_corner(LEFT), direction=RIGHT, buff = 0, aligned_edge=LEFT)),
                    nth_deriv_start[0][15:17].animate.shift((MathTex(r"\frac{(n-1)!}{x^n}")[0][6].scale(text_scale+0.1).next_to(nth_deriv_start[0][14].get_corner(LEFT), direction=RIGHT, buff = 0, aligned_edge=LEFT).get_x()-nth_deriv_start[0][15:17].get_x())*RIGHT))
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

            self.play(Transform(nth_deriv_start[0][8:11], MathTex(r"(-1)^{n+1}").scale(text_scale+0.1).next_to(nth_deriv_start[0][8:11].get_corner(LEFT), direction=RIGHT, buff = 0, aligned_edge=LEFT)),
                    nth_deriv_start[0][11:].animate.shift((MathTex(r"(-1)^{n+1}").scale(text_scale+0.1).next_to(nth_deriv_start[0][8:11].get_corner(LEFT), direction=RIGHT, buff = 0, aligned_edge=LEFT).get_corner(RIGHT)[0]-nth_deriv_start[0][10].get_corner(RIGHT)[0])*RIGHT))
        
        setup_graph()
        calculate_derivatives()

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