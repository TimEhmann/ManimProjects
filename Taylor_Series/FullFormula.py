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
    x_sym = sympy.symbols('x')
    a_sym = sympy.sympify(a)  # Keep 'a' symbolic
    x_sym = sympy.sympify(x)  # Keep 'x' symbolic

    val = 0
    for n in range(n_terms + 1):
        deriv_at_a = f_deriv(f, a_sym, n)  # Use symbolic derivative
        term = deriv_at_a / sympy.factorial(n) * (x_sym - a_sym)**n
        val += term

    # Convert to float only at the end for numerical stability
    val = float(val)

    # Cap the output value
    if abs(val) > 5:  # Limit based on axes range
        return math.copysign(5, val)
    return val

X_SYM = sympy.symbols('x')
COS = sympy.cos(X_SYM)

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
