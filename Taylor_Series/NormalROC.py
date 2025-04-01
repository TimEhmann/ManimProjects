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

class RadiusOfConvergence_v2(Scene):
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
            x_sym = sympy.symbols('x')
            f_expr = sympy.log(x_sym)
            for i in range(11):
                func = lambda x: taylor_approx_at_a(f_expr, x, 1, i)
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
                    graph = axes.plot(lambda x: taylor_approx_at_a(f_expr, x, 2, i), x_range=[0.01, 4.5, 0.01], color=ORANGE)
                    #Transform infinity to 0, color T(x) orange
                    self.play(Transform(taylor_formula[0][5], MathTex(i).scale(0.5).next_to(taylor_formula[0][5].get_center(), direction=0, buff = 0.0, aligned_edge=ORIGIN)),
                              taylor_formula[0][:4].animate.set_color(ORANGE), run_time=0.4)
                    self.wait(0.2)
                    self.play(Write(graph), run_time=0.4)
                else:
                    self.play(Transform(graph, axes.plot(lambda x: taylor_approx_at_a(f_expr, x, 2, i), x_range=[0.01, 4.5, 0.01], color=ORANGE)),
                              Transform(taylor_formula[0][5], MathTex(i).scale(0.5).next_to(taylor_formula[0][5].get_center(), direction=0, buff = 0.0, aligned_edge=ORIGIN)), run_time=0.4)
                self.wait(0.2)

            # show interval and radius again. This time its (0,4) and the radius is 2
            brace = BraceBetweenPoints(axes.coords_to_point(0,0), axes.coords_to_point(4,0), direction=UP, color=RED)
            text = brace.get_text("Convergence Interval = (0,4)").scale(0.5).shift(0.2*DOWN).add_background_rectangle()
            self.play(GrowFromCenter(brace), Write(text))
            self.wait()
            brace_2 = BraceBetweenPoints(axes.coords_to_point(2,0), axes.coords_to_point(4,0), direction=DOWN, color=RED_D)
            text_2 = brace_2.get_text("Radius of Convergence = 2").scale(0.5)
            self.play(GrowFromCenter(brace_2), Write(text_2))
            self.wait()

            self.play(FadeOut(text), FadeOut(brace), FadeOut(text_2), FadeOut(brace_2), FadeOut(graph), FadeOut(dot_2), FadeOut(taylor_formula))
            self.wait()
        
        def show_general_radius():
            """Visualizes the general radius of convergence based on singularity."""
            # Keep axes and log graph visible

            # --- General Case Visualization ---
            title = Tex("General Case: Radius of Convergence for $f(x)=\ln(x)$", font_size=36).to_edge(UP)
            self.play(Write(title))
            self.wait(0.5)

            # Check if singularity is within y-axis range before drawing line
            y_ax_min, y_ax_max = axes.y_range[:2]
            singularity_line = DashedLine(
                axes.c2p(0, y_ax_min),
                axes.c2p(0, y_ax_max),
                color=RED, stroke_width=3
            )
            singularity_label = Tex("Singularity!", color=RED, font_size=28).next_to(axes.c2p(0, 1.5), RIGHT, buff=0.1)

            self.play(Create(singularity_line), Write(singularity_label))
            self.wait(1)

            # General center 'a' (ValueTracker)
            initial_a = 1.5
            a_val = ValueTracker(initial_a)

            # Dot representing 'a' on the x-axis (used for vertical line later)
            a_dot = Dot(color=YELLOW, radius=0.08)
            # Label 'a' - initially empty, updated relative to brace
            a_label = MathTex("a", color=YELLOW).scale(0.8)

            # Radius line (from a to singularity at x=0)
            radius_line = Line(color=YELLOW, stroke_width=5)
            radius_line.add_updater(
                lambda m: m.put_start_and_end_on(
                    axes.c2p(a_val.get_value(), 0), # Start at 'a' on x-axis
                    axes.c2p(0, 0)                  # End at singularity (origin)
                )
            )

            # Radius Brace and Text (with updaters)
            radius_brace = Brace(radius_line, direction=DOWN, color=YELLOW) # Initial dummy brace
            radius_text = MathTex("R = a", color=YELLOW).scale(0.7)

            def radius_brace_updater(mob): # mob is radius_brace
                current_a = a_val.get_value()
                # Only update if 'a' is positive and line has significant length
                if current_a > 1e-3 and radius_line.get_length() > 1e-3:
                    # Recreate brace based on current line geometry
                    new_brace = Brace(radius_line, direction=DOWN, color=YELLOW)
                    mob.become(new_brace) # Keep become here to update shape based on line

                    # Update radius text content and position
                    new_radius_text = MathTex(f"R = {current_a:.1f}", color=YELLOW).scale(0.7)
                    new_radius_text.next_to(mob, DOWN, buff=0.1)
                    radius_text.become(new_radius_text) # Use become to replace text content

                    # --- FIX for Issue 1: Update 'a' label position ---
                    # Position 'a' label near the start of the brace (where 'a' is)

                    # --- ADD THIS CHECK ---
                    if mob.has_points():
                        a_label_target_pos = mob.get_start() + DOWN * 0.4 # Position below start
                        a_label.move_to(a_label_target_pos)
                        if not a_label.has_points(): # Ensure it becomes visible if it was empty
                            a_label.set_opacity(1)
                            # If a_label became VMobject(), setting opacity might not be enough.
                            # A safer approach if it truly becomes VMobject() might be needed,
                            # but let's try this first. Consider changing the 'else' block
                            # below to just set opacity=0 instead of become(VMobject()).
                    else:
                        # If mob has no points even in this branch (e.g., during animation start)
                        # make the label disappear to prevent errors/flickering.
                        a_label.become(VMobject()) # Or a_label.set_opacity(0)

                else:
                    # If a is too small or zero, make brace have no points and text empty
                    mob.set_points(np.zeros((0, 3))) # Safer: Make brace have no points
                    radius_text.become(VMobject()) # Keep this for the text
                    # --- FIX for Issue 1: Hide 'a' label ---
                    a_label.become(VMobject()) # Make 'a' label disappear

            radius_brace.add_updater(radius_brace_updater)
            # --- REMOVE old a_label updater ---
            # a_label.add_updater(lambda m: m.next_to(a_dot, DOWN, buff=0.15)) # REMOVED


            # Interval Brace and Text (with updaters)
            interval_brace = Brace(Line(LEFT, RIGHT), direction=UP, color=BLUE) # Initial dummy
            interval_text = MathTex("(0, 2a)", color=BLUE).scale(0.7)

            def interval_updater(mob): # mob is interval_brace
                current_a = a_val.get_value()
                start_x_interval = 0
                end_x_interval = 2 * current_a
                plot_start_x = max(axes.x_range[0], start_x_interval) + 0.01
                plot_end_x = min(axes.x_range[1], end_x_interval)

                if plot_end_x > plot_start_x and current_a > 1e-3:
                    new_brace = BraceBetweenPoints(
                        axes.c2p(plot_start_x, 0),
                        axes.c2p(plot_end_x, 0),
                        direction=UP, color=BLUE
                    )
                    mob.become(new_brace)
                    new_interval_text = MathTex(f"(0, {end_x_interval:.1f})", color=BLUE).scale(0.7)
                    new_interval_text.next_to(mob, UP, buff=0.1)
                    interval_text.become(new_interval_text)
                else:
                    mob.set_points(np.zeros((0, 3)))
                    interval_text.become(VMobject())

            interval_brace.add_updater(interval_updater)

            # --- Approximation Graph Setup ---
            approx_graph_dynamic = VMobject().set_z_index(-1) # Put behind axis lines/labels
            approx_graph_dynamic._last_a_value = None # Initialize

            # --- Moving Dot and Vertical Line Setup ---
            vertical_line = DashedLine(stroke_width=2, color=YELLOW, stroke_opacity=0.7)
            # func = lambda x: math.log(x) # Define func if not already available

            def dot_line_updater(mob): # mob is dummy_updater_mob
                a = a_val.get_value()
                y_val = 0 # Default y
                try:
                    # Make sure func is defined or use math.log directly
                    y_val = math.log(a) # Using math.log directly
                except ValueError: # Handle log(a) for a<=0
                    pass # Keep y_val = 0
                if not np.isfinite(y_val): y_val = 0

                graph_point = axes.c2p(a, y_val)
                a_dot.move_to(graph_point) # a_dot moves on the log graph now
                vertical_line.put_start_and_end_on(graph_point, axes.c2p(a, 0))

            dummy_updater_mob = Mobject().add_updater(dot_line_updater)


            # --- OPTIMIZED Updater for Dynamic Approximation Graph ---
            def approx_graph_updater(mob): # mob is approx_graph_dynamic
                current_a = a_val.get_value()
                if current_a <= 0: # Skip if center is invalid
                    mob.become(VMobject())
                    mob._last_a_value = current_a
                    return

                previous_a = getattr(mob, '_last_a_value', None)
                tolerance = 1e-5 # Adjusted tolerance slightly

                a_has_changed = (previous_a is None) or (abs(current_a - previous_a) > tolerance)

                if a_has_changed:
                    # print(f"Recalculating graph for a = {current_a}") # Debug
                    a = current_a
                    R = a # Radius for ln(x) centered at a is a
                    # Define plot range based on ROC (0, 2a), slightly extended
                    plot_start = max(0.01, axes.x_range[0]) # Start near 0
                    plot_end = min(2 * a + 1, axes.x_range[1]) # End near 2a + buffer

                    new_graph_generated = False
                    if plot_end > plot_start + 0.05:
                        try:
                            # --- FIX for Issue 2: Use correct function ---
                            # Assuming 10 terms for approximation
                            x_sym = sympy.symbols('x')
                            f_expr = sympy.log(x_sym)
                            current_approx_func = lambda x: taylor_approx_at_a(f_expr, x, a, 10)

                            x_values = np.linspace(plot_start, plot_end, num=100) # Reduced points slightly
                            y_values = np.array([current_approx_func(x) for x in x_values])

                            # Filter out non-finite values
                            valid_indices = np.isfinite(y_values) # Keep only finite
                            x_values = x_values[valid_indices]
                            y_values = y_values[valid_indices]

                            # Further filter extreme values if needed (optional)
                            y_limit = 10 # Example limit
                            valid_indices_lim = np.abs(y_values) < y_limit
                            x_values = x_values[valid_indices_lim]
                            y_values = y_values[valid_indices_lim]

                            if len(x_values) > 1:
                                new_graph = axes.plot_line_graph(
                                    x_values=x_values, y_values=y_values,
                                    line_color=ORANGE, stroke_width=3, # Slightly thinner
                                    add_vertex_dots=False
                                )
                                mob.become(new_graph)
                                new_graph_generated = True
                        except Exception as e:
                            print(f"Error during graph generation for a={a}: {e}") # Print errors

                    if not new_graph_generated:
                        mob.become(VMobject())

                    mob._last_a_value = current_a


            approx_graph_dynamic.add_updater(approx_graph_updater)

            # --- Add Objects with Updaters to Scene ---
            self.play(FadeIn(radius_line), FadeIn(radius_brace), FadeIn(radius_text), FadeIn(interval_brace), FadeIn(interval_text),
                      FadeIn(dummy_updater_mob), FadeIn(a_dot), FadeIn(a_label), FadeIn(vertical_line), Create(approx_graph_dynamic))


            # --- Initial Creation Animations (Optional but Recommended) ---
            # Instead of just adding, maybe animate creation?
            # Need to call updaters once manually before animating creation
            dot_line_updater(dummy_updater_mob)
            radius_brace_updater(radius_brace)
            interval_updater(interval_brace)
            approx_graph_updater(approx_graph_dynamic) # Calculate initial graph state

            # Play creation animations
            initial_create_anims = [
                Create(a_dot), Write(a_label), Create(vertical_line),
                Create(radius_line), GrowFromCenter(radius_brace), Write(radius_text),
                GrowFromCenter(interval_brace), Write(interval_text),
            ]
            # Only add graph creation if it has points initially
            if approx_graph_dynamic.has_points():
                initial_create_anims.append(Create(approx_graph_dynamic))

            # Filter out animations for potentially empty objects
            initial_create_anims_filtered = [anim for anim in initial_create_anims if anim.mobject.has_points()]

            if initial_create_anims_filtered:
                self.play(*initial_create_anims_filtered, run_time=1.5)
            else:
                print("Warning: Could not create initial general radius elements via animation.")
                # Objects were already added, so they should appear if they have points.

            self.wait(1)


            # --- Animate 'a' changing ---
            explanation_text = Tex(
                "Distance from center $a$ to singularity at $x=0$ determines radius $R=a$.",
                font_size=28
            ).next_to(title, DOWN, buff=0.3)
            self.play(Write(explanation_text))
            self.wait(1)

            target_a_values = [1.0, 2.5, 0.5, initial_a] # Adjusted target values
            run_times = [2.5, 3.0, 2.5, 1.5] # Adjusted run times

            for target_a, rt in zip(target_a_values, run_times):
                self.play(a_val.animate.set_value(target_a), run_time=rt)
                # No wait needed here, updaters handle changes during animation
            self.wait(1) # Pause at the final position


            # --- Final Conclusion Text ---
            conclusion = Tex(
                r"Taylor series for $\ln(x)$ centered at $a>0$ converges on $(0, 2a)$ with radius $R=a$.",
                font_size=32
            ).next_to(axes, DOWN, buff=0.5).shift_onto_screen()
            self.play(Write(conclusion))
            self.wait(3)

            # --- Cleanup Updaters and Fade Out ---
            print("Clearing updaters...") # Debug print
            # Important: Remove dummy updater mob first to stop its updater
            self.remove(dummy_updater_mob)
            # Then clear updaters from the actual objects
            mobjects_with_updaters = [
                a_dot, a_label, radius_line, radius_brace, interval_brace,
                approx_graph_dynamic, radius_text, interval_text # Include texts just in case
                ]
            for mobj in mobjects_with_updaters:
                # Check if object exists before clearing, belt-and-braces
                if mobj is not None:
                    mobj.clear_updaters()

            print("Fading out general explanation elements...") # Debug print
            elements_to_fade_general = [
                title, singularity_line, singularity_label,
                a_dot, a_label, radius_line, radius_brace, radius_text,
                interval_brace, interval_text, vertical_line,
                approx_graph_dynamic, # Include the dynamic graph
                explanation_text, conclusion
                ]
            # Filter out any potentially empty/None VMobjects again
            elements_to_fade_general = [m for m in elements_to_fade_general if m and m.has_points()]

            if elements_to_fade_general:
                self.play(*[FadeOut(m) for m in elements_to_fade_general])
            else:
                print("Warning: No elements to fade out.") # Debug print
            self.wait(1)
        
        setup_graph()
        calculate_derivatives()
        show_general_radius()
