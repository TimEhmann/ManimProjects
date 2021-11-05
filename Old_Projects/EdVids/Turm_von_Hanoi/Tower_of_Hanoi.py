from manim import *
import numpy as np

class TurmVonHanoi(Scene):

    def construct(self):
        series_rek = MathTex(r"a_{n}",r"=",r"2\cdot a_{n-1}",r"+1")
        series_change = [MathTex(r"a_{n}=2\cdot ", r"a_{n-1}", r"+1"), 
                        MathTex(r"a_{n}=2\cdot2\cdot", r"a_{n-2}", r"+2+1"),
                        MathTex(r"a_{n}=", r"2\cdot2\cdot2", r"\cdot a_{n-3}",r"+2\cdot2", r"+2", r"+1"),
                        MathTex(r"\vdots"), 
                        MathTex(r"a_{n}=", r"2\cdot\ldots", r"\cdot ", r"a_{n-(n-1)}", r"+", r"2\cdot\ldots\cdot2", r"+\ldots+", r"2", r"+", r"1"), 
                        MathTex(r"a_{n}=", r"2^{n-1}", r"\cdot", r"1", r"+", r"2^{n-2}", r"+\ldots+", r"2^{1}", r"+", r"2^{0}"),
                        MathTex(r"a_{n}=\sum_{i=0}^{n-1}2^{i}"), 
                        MathTex(r"a_{n}=\frac{1-2^{n-1+1}}{1-2}"), 
                        MathTex(r"a_{n}=2^{n}-1")]
        geometric_series = MathTex(r"\sum_{i=0}^{n}q^{i}=\frac{1-q^{n+1}}{1-q}")

        self.play(Write(series_rek.scale(0.8).to_corner(UL)))
        self.wait()
        self.add(series_change[0].scale(0.8).to_corner(UL))
        self.play(series_change[0].animate.shift(0.55*DOWN))
        self.wait()
        self.play(series_change[0][1].animate.set_fill(RED), series_rek[0].animate.set_fill(RED))
        self.wait()
        
        #einsetzen von a_n in a_n-1
        temp = MathTex(r"(2\cdot", r"a_{n-2}", r"+1)").scale(0.8)
        temp.shift(series_change[0][0].get_corner(RIGHT)-temp.get_corner(LEFT)+0.1*RIGHT+0.01*DOWN)
        self.play(ReplacementTransform(series_rek[2].copy(), temp), FadeOut(series_change[0][1]), series_change[0][2].animate.shift(1.4*RIGHT))
        self.wait()
        
        #ausmultiplizieren
        self.play(Write(series_change[1].scale(0.8).next_to(series_change[0], DOWN, aligned_edge= LEFT)))
        self.wait()
        self.play(series_change[1][1].animate.set_fill(RED))

        #nochmal einsetzen
        temp2 = MathTex(r"(2\cdot", r"a_{n-3}", r"+1)").scale(0.8)
        temp2.shift(series_change[1][0].get_corner(RIGHT)-temp2.get_corner(LEFT)+0.1*RIGHT+0.01*DOWN)
        self.play(ReplacementTransform(series_rek[2].copy(), temp2), FadeOut(series_change[1][1]), series_change[1][2].animate.shift(1.4*RIGHT))
        self.wait()
        self.play(series_rek[0].animate.set_fill(WHITE))

        #ausmultiplzieren
        self.play(Write(series_change[2].scale(0.8).next_to(series_change[1], DOWN, aligned_edge= LEFT)))
        self.wait()

        #vdots
        self.play(Write(series_change[3].scale(0.8).next_to(series_change[2], DOWN)))
        self.wait()

        #marks
        self.play(series_rek[-1][-1].animate.set_fill(RED), series_change[0][-1][-1].animate.set_fill(RED), series_change[1][-1][-1].animate.set_fill(RED),series_change[2][-1][-1].animate.set_fill(RED))
        self.play(series_change[0][0][3].animate.set_fill(ORANGE), series_change[1][2][1].animate.set_fill(ORANGE), series_change[2][-2][1].animate.set_fill(ORANGE), temp[-1][-2].animate.set_fill(ORANGE))
        self.play(series_change[1][0][3].animate.set_fill(YELLOW), series_change[1][0][4].animate.set_fill(YELLOW), series_change[1][0][5].animate.set_fill(YELLOW),series_change[2][3][1].animate.set_fill(YELLOW),series_change[2][3][2].animate.set_fill(YELLOW),series_change[2][3][3].animate.set_fill(YELLOW), temp2[-1][-2].animate.set_fill(YELLOW))
        self.play(series_change[2][1].animate.set_fill(GREEN))
        
        #dots
        self.play(Write(series_change[4].scale(0.8).next_to(series_change[3], DOWN).to_edge(LEFT)))
        self.wait()

        #rectangels
        framebox1 = SurroundingRectangle(series_change[2][1], buff = .1)
        exp_1 = MathTex(r"2^{3}").scale(0.8).next_to(framebox1, DOWN, buff = .1).set_color(GREEN)
        framebox2 = SurroundingRectangle(series_change[2][3], buff = .1)
        exp_2 = MathTex(r"2^{2}").scale(0.8).next_to(framebox2, DOWN, buff = .1).set_color(YELLOW)
        framebox3 = SurroundingRectangle(series_change[2][4], buff = .1)
        exp_3 = MathTex(r"2^{1}").scale(0.8).next_to(framebox3, DOWN, buff = .1).set_color(ORANGE)
        framebox4 = SurroundingRectangle(series_change[2][5], buff = .1)
        exp_4 = MathTex(r"2^{0}").scale(0.8).next_to(framebox4, DOWN, buff = .1).set_color(RED)
        self.play(Create(framebox1), Write(exp_1))
        self.wait()
        self.play(Transform(framebox1, framebox2), Transform(exp_1, exp_2))
        self.wait()
        self.play(Transform(framebox1, framebox3), Transform(exp_1, exp_3))
        self.wait()
        self.play(Transform(framebox1, framebox4), Transform(exp_1, exp_4))
        self.wait()

        #dots in richtig
        self.play(Write(series_change[5].scale(0.8).next_to(series_change[4], DOWN).to_edge(LEFT)))
        self.wait()
        self.play(series_change[4][1].animate.set_fill(BLUE), series_change[5][1].animate.set_fill(BLUE),
                  series_change[4][3].animate.set_fill(TEAL), series_change[5][3].animate.set_fill(TEAL),
                  series_change[4][5].animate.set_fill(GOLD), series_change[5][5].animate.set_fill(GOLD),
                  series_change[4][7].animate.set_fill(MAROON), series_change[5][7].animate.set_fill(MAROON),
                  series_change[4][9].animate.set_fill(PINK), series_change[5][9].animate.set_fill(PINK)
        )
        self.wait()
        self.play(FadeOut(framebox1), FadeOut(exp_1))
        self.wait()

        #sum
        self.play(Write(series_change[6].scale(0.8).next_to(series_change[5], DOWN).to_edge(LEFT)))
        self.wait()

        #geometric series
        self.play(Write(geometric_series.scale(0.8).next_to(series_change[6], RIGHT, buff = 2)))
        self.wait()

        #solution
        self.play(Write(series_change[7].scale(0.8).next_to(series_change[6], DOWN).to_edge(LEFT)))
        self.wait()
        self.play(Write(series_change[8].scale(0.8).next_to(series_change[7], DOWN).to_edge(LEFT)))
        self.wait()
        self.play(Create(SurroundingRectangle(series_change[8], buff=.1)))

class Binary(Scene):
    def construct(self):
        p_o_2 = MathTex(r"2^{n}").to_corner(UL).shift(RIGHT+0.25*DOWN)
        binary = Text("Als Binärzahl").scale(0.8).to_edge(UP).shift(0.5*LEFT+0.25*DOWN)
        summe = MathTex(r"\sum_{i=0}^{n}2^{i}").scale(0.8).to_corner(UR).shift(LEFT)
        l1 = Line(4*UP+4*LEFT,4*DOWN+4*LEFT)
        l2 = Line(4*UP-3*LEFT,4*DOWN-3*LEFT)
        self.add(l1,l2, p_o_2, binary, summe)
        first = MathTex(r"2^{0}")