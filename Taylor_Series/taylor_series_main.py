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
        x_scale_factor = 2.5
        x_labels = [
            MathTex("-5\pi"),MathTex("-4\pi"),MathTex("-3\pi"), MathTex("-2\pi"), MathTex ("-\pi"), 
            MathTex("0"), 
            MathTex("\pi"), MathTex("2\pi"), MathTex("3\pi"), MathTex("4\pi"), MathTex("5\pi")
        ]
        plot = VGroup()
        for i in range(len(x_labels)):
            x_labels[i].add_background_rectangle().next_to(np.array([ x_scale_factor*(-6 + 12/(11*np.pi) + (6-12/(11*np.pi))/5*i), 0, 0]), 0.5*DOWN).scale(0.7)
            self.add_foreground_mobject(x_labels[i])
            plot = VGroup(x_labels[i], plot)
        sin_graph = axes.get_graph(lambda x: taylorseries_sine(x,15), color = GREEN)
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


class cosapproximationGoal(Scene):
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
    
        approximation_term_parts = [MathTex("f(x) = ").set_color(GREEN).to_corner(UL), MathTex("1"), MathTex(r"-\frac{x^{2}}{2}"),
            MathTex(r"+\frac{x^{4}}{24}"), MathTex(r"-\frac{x^{6}}{720}"), MathTex(r"+\frac{x^{8}}{40320}"), MathTex(r"-\frac{x^{10}}{3628800}"),
            MathTex(r"+\frac{x^{12}}{479001600}"), MathTex(r"\cdots")]
        def show_cosine_approximation_n_to_m(start_degree, finish_degree):
            self.play(Write(approximation_term_parts[0]))
            for i in range(start_degree, finish_degree+1):
                if i == start_degree:
                    cos_appr = axes.get_graph(lambda x: taylorseries_cosine(x, i), color = GREEN)
                    approximation_term_parts[i+1].scale(0.8).next_to(approximation_term_parts[i]).set_color(GREEN)
                    self.play(Create(cos_appr), Write(approximation_term_parts[i+1]))
                    self.wait()
                else:
                    next_iteration = axes.get_graph(lambda x: taylorseries_cosine(x, i), color = GREEN)
                    if i < len(approximation_term_parts)-1:
                        approximation_term_parts[i+1].scale(0.8).next_to(approximation_term_parts[i]).set_color(GREEN)
                        self.play(Transform(cos_appr, next_iteration), Write(approximation_term_parts[i+1]))
                    else:
                        self.play(Transform(cos_appr, next_iteration))
                    self.wait()

        show_cosine_approximation_n_to_m(0,10)

class cosApproximationTut(ZoomedScene):
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
            MathTex("-2\pi"), MathTex ("-\pi"), 
            MathTex(""), 
            MathTex("\pi"), MathTex("2\pi")
        ]
        for i in range(len(x_labels)):
            x_labels[i].add_background_rectangle().next_to(np.array([-26/4.4+i*13/4.4, 0, 0]), DOWN).scale(0.7)
            plot = VGroup(plot, x_labels[i])
        cos_graph = axes.get_graph(lambda x: math.cos(x) , color = GREEN)
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
                    axes.get_graph(
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
                    axes.get_graph(
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
                    axes.get_graph(
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
            approximation_graph = axes.get_graph(lambda x: 1, color = apprx_color)
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
            self.play(Transform(approximation_graph, axes.get_graph(lambda x: 1-x**2/2).set_color(apprx_color)))
            self.wait()
        
        first_order()
        second_order()
        third_order()

        #first_order_calc()
        #second_order_calc()
        #third_order_calc()

        

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