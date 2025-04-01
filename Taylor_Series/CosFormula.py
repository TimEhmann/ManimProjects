'''
In this scene, the Taylor Series for cos(x) is kind of mathematically derived (deriving based on pattern recognition)
'''

from manim import *
import math
import scipy as sp
import sympy
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
