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
COS = math.cos(X_SYM)

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
            self.play(Transform(approximation_graph, axes.plot(lambda x: taylor_approx_at_a(COS, x, 0, 5)).set_color(apprx_color)),
                        Write(new_term))
            self.wait()

            new_term = MathTex(r'-\frac{x^6}{720}').scale(0.8).set_color(apprx_color).next_to(new_term, direction=RIGHT, buff = 0.1)
            function_term.add(new_term)
            self.play(Transform(approximation_graph, axes.plot(lambda x: taylor_approx_at_a(COS, x, 0, 7)).set_color(apprx_color)),
                        Write(new_term))
            self.wait()

            new_term = MathTex(r'+\frac{x^8}{40320}').scale(0.8).set_color(apprx_color).next_to(new_term, direction=RIGHT, buff = 0.1)
            function_term.add(new_term)
            self.play(Transform(approximation_graph, axes.plot(lambda x: taylor_approx_at_a(COS, x, 0, 9)).set_color(apprx_color)),
                        Write(new_term))
            self.wait()

            new_term = MathTex(r'-\frac{x^{10}}{3628800}').scale(0.8).set_color(apprx_color).next_to(new_term, direction=RIGHT, buff = 0.1)
            function_term.add(new_term)
            self.play(Transform(approximation_graph, axes.plot(lambda x: taylor_approx_at_a(COS, x, 0, 11)).set_color(apprx_color)),
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
