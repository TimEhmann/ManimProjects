from manimlib.imports import *
import numpy as np
import math
import functools

number_of_terms = 10

##TO DO
#
#
#

#wird diese anstatt der allgemeinen Taylorpolynom Berechnung verwendet,
#sind mehr Annäherungsterme möglich, da in TP Berechnung bei zu hoher Termanzahl
#die Berechnung zusammenfällt, da Computer nicht mit den Werten klarkommt, genauer
#Fehler ist mir jedoch unklar
def taylor_approximation_cos(k,x):
    value = 0
    for i in range(k):
        value = value + ((x**(2*i)*(-1)**i)/math.factorial(2*i))
    return value

class CosApproximationTut(GraphScene):
    CONFIG = {
        "x_min" : -2*np.pi,
        "x_max" : 2*np.pi,
        "x_tick_frequency" : np.pi/2,
        "x_axis_label": "$x$",
        "x_axis_width": 13,
        #"x_labeled_nums": np.arange(-8,10,2),
        "y_min" : -2,
        "y_max" : 2,
        "y_tick_frequency" : 1, 
        #"y_axis_label": "$f(x)$",
        #"y_labeled_nums": np.arange(-4,5,1),
        "graph_origin": 1*DOWN,
    }

    def setup(self):            
        GraphScene.setup(self)

    def construct(self):
        self.setup_axes(animate=True)
        self.add_cosine_graph()
        self.first_approximation()
        self.second_approximation()
        self.third_approximation()

    def add_cosine_graph(self):
        
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

    def first_approximation(self):

        #####################
        #LEFT SIDE OF SCREEN#
        #####################
        self.wait(5)
        placeholder = TexMobject("f'''(x) = -cos(x)") #wird nicht verwendet, nur placeholder
        placeholder.scale(0.6).to_corner(UL)
        cos_eq = TexMobject("f(x) = cos(x)").set_color(BLUE)
        cos_eq.scale(0.6).next_to(placeholder, DOWN, aligned_edge = RIGHT).to_edge(LEFT)
        self.play(Write(cos_eq))

        #Spaltentrennungslinie zeichnen
        l = Line(6*DOWN + RIGHT)
        l.next_to(placeholder)
        self.play(ShowCreation(l))

        #bei x = 0 als zweite Spalte
        x_eql_0text = TextMobject("bei ")
        x_eql_0text.scale(0.6)
        x_eql_0 = TexMobject("x = 0")
        x_eql_0.scale(0.6)
        sentence=VGroup(x_eql_0text,x_eql_0)
        sentence.arrange_submobjects(RIGHT, buff=0.1).next_to(placeholder, RIGHT, buff = 0.5)
        self.play(Write(sentence))
        #self.play(Write(x_eql_0text))
        #self.play(Write(x_eql_0))

        self.wait(4)
        #cos is equal to 1
        cos_eql_1 = TexMobject("1")
        cos_eql_1.set_color(PINK)
        cos_eql_1.scale(0.6).next_to(cos_eq, RIGHT, buff = 1.55)
        self.play(Write(cos_eql_1))

        ######################
        #RIGHT SIDE OF SCREEN#
        ######################

        self.wait(15)
        #L1 CREATING T(x)

        aprx_eq = TexMobject(r"\\T(x)", "=", "a")
        aprx_eq[0].set_color(ORANGE)
        aprx_eq[2].set_color(YELLOW)
        aprx_eq.to_corner(UR)

        #SHOW T(x) IN THE TOP RIGHt
        
        self.play(Write(
            aprx_eq,
            run_time = 2
        ))
        self.wait(6)

        #SHOWING THE INFLUENCE a HAS ON THE GRAPH

        #GRAPHING A LINE PARALLEL TO THE X-AXSIS
        a = 0
        graph = self.get_graph(lambda x: a, x_min = self.x_min, x_max = self.x_max).set_color(ORANGE)
        self.play(ShowCreation(graph), run_time=3)
        self.wait(1)
        #CHANING INPUT a
        a = [0.5, -0.75, 1.5, -1, 1]
        for n in a:
            new_graph = self.get_graph(lambda x: n, x_min = self.x_min, x_max = self.x_max).set_color(ORANGE)
            self.play(
                Transform(graph, new_graph, run_time=2.5),
            )
        
        self.wait(9)
        #HOW TO CALCULATE a
        
        #L2 PLUGGING IN 0 INTO T(x)
        
        aprx_eq2 = TexMobject(r"\\T(0)", "=", "a")
        aprx_eq2[0].set_color(ORANGE) #colouring a yellow
        aprx_eq2[2].set_color(YELLOW) #colouring a yellow
        aprx_eq2.next_to(aprx_eq.get_part_by_tex("T"), DOWN, aligned_edge = LEFT)

        #SHOWING T(0) UNDERNEATH T(x)

        self.play(FadeIn(aprx_eq2,run_time = 2))
        self.wait(4)

        #L3 SOLVING FOR A

        aprx_eq3 = TexMobject(r"\\1 ", "=", "a")
        aprx_eq3[0].set_color(PINK) #colouring 1 pink
        aprx_eq3[2].set_color(YELLOW) #colouring a yellow
        aprx_eq3.next_to(aprx_eq2, DOWN,)

        #MOVING SOLVED A UNDERNEATH T(0)

        self.play(FadeIn(aprx_eq3,run_time = 2))
        self.wait(3)
        #L1 NEW T(x)

        aprx_eq_new = TexMobject(r"\\T(x)", "=", "1")
        aprx_eq_new[0].set_color(ORANGE)
        aprx_eq_new[2].set_color(YELLOW)

        #TRANSFORMING L1 
        
        aprx_eq_new.next_to(aprx_eq2.get_part_by_tex("T"), UP, aligned_edge = LEFT)
        self.play(Transform(
            aprx_eq,
            aprx_eq_new,
            run_time = 2
        ))
        self.wait(4)
        
        #Fade out all the Terms
        self.play(
            FadeOutAndShift(aprx_eq , direction=RIGHT),
            FadeOutAndShift(aprx_eq2, direction=RIGHT),
            FadeOutAndShift(aprx_eq3, direction=RIGHT),
        )
        self.remove(cos_eq, sentence, l, cos_eql_1, graph)

    def second_approximation(self):

        #################
        #TO DO
        #at b = 1/-1 it would be correct if center_point was -pi/2 or pi/2
        
        ##################
        #ADDING THE GRAPH#
        ##################
        graph = self.get_graph(functools.partial(taylor_approximation_cos, 1), x_min = self.x_min, x_max = self.x_max).set_color(ORANGE)
        self.add(graph)

        #####################
        #LEFT SIDE OF SCREEN#
        #####################

        placeholder = TexMobject("f'''(x) = -cos(x)") #wird nicht verwendet, nur placeholder
        placeholder.scale(0.6).to_corner(UL)
        cos_eq = TexMobject("f(x) = cos(x)").set_color(BLUE)
        cos_eq.scale(0.6).next_to(placeholder, DOWN, aligned_edge = RIGHT).to_edge(LEFT)
        self.add(cos_eq)

        #Spaltentrennungslinie zeichnen
        l = Line(6*DOWN + RIGHT)
        l.next_to(placeholder)
        self.add(l)

        #bei x = 0 als zweite Spalte
        x_eql_0text = TextMobject("bei ")
        x_eql_0text.scale(0.6)
        x_eql_0 = TexMobject("x = 0")
        x_eql_0.scale(0.6)
        sentence=VGroup(x_eql_0text,x_eql_0)
        sentence.arrange_submobjects(RIGHT, buff=0.1).next_to(placeholder, RIGHT, buff = 0.5)
        self.add(sentence)
        #self.play(Write(x_eql_0text))
        #self.play(Write(x_eql_0))

        #cos is equal to 1
        f_eql_1 = TexMobject("1")
        f_eql_1.scale(0.6).next_to(cos_eq, RIGHT, buff = 1.55)
        self.add(f_eql_1)

        #NEW STUFF
        self.wait(8)
        #cos derivative (-sin) underneath cos
        cos_deriv_1 = TexMobject("f'(x) = -sin(x)")
        cos_deriv_1.scale(0.6)
        cos_deriv_1.next_to(cos_eq, DOWN).to_edge(LEFT)
        self.play(ReplacementTransform(cos_eq.copy(), cos_deriv_1))
        
        #-sin is equal to 0
        self.wait(3)
        f_eql_0 = TexMobject("0")
        f_eql_0.set_color(PINK)
        f_eql_0.scale(0.6).next_to(cos_deriv_1, RIGHT, buff = 1.22)
        self.play(ReplacementTransform(cos_deriv_1.copy(), f_eql_0))
        
        ######################
        #RIGHT SIDE OF SCREEN#
        ######################
        
        self.wait(6)
        #L1 CREATING T(x)

        aprx_eq = TexMobject(r"\\T(x)", "=", "1", "+", "b", "x")
        aprx_eq[0].set_color(ORANGE)
        aprx_eq[2].set_color(YELLOW)
        aprx_eq[4].set_color(RED)
        aprx_eq.scale(0.8).to_corner(UR)

        #SHOW T(x) IN THE TOP RIGHT
        
        self.play(Write(
            aprx_eq,
            run_time = 2
        ))

        self.wait(10)

        #SHOWING THE INFLUENCE b HAS ON THE GRAPH
        #CHANING INPUT b
        b = [0.5, -0.75, 1, 0.25]
        for n in b:
            new_graph = self.get_graph(lambda x: 1+n*x, x_min = self.x_min, x_max = self.x_max).set_color(ORANGE)
            self.play(
                Transform(graph, new_graph, run_time=3),
            )
        

        self.wait(10)

        #HOW TO CALCULATE b

        #L2 Derivative of T(x)
        
        aprx_eq_deriv = TexMobject(r"\\{T}'(x) =", "b")
        aprx_eq_deriv[1].set_color(RED)
        aprx_eq_deriv.scale(0.8).next_to(aprx_eq.get_part_by_tex("T"), DOWN, aligned_edge = LEFT)

        #Transforming T(x) into T'(x)

        self.play(ReplacementTransform(aprx_eq.copy(), aprx_eq_deriv))
        self.wait(7)

        #L3 PLUGGING 0 INTO T'(x)
        
        aprx_eq_deriv2 = TexMobject(r"\\{T}'(0) =", "b")
        aprx_eq_deriv2[1].set_color(RED)
        aprx_eq_deriv2.scale(0.8).next_to(aprx_eq_deriv.get_part_by_tex("T"), DOWN, aligned_edge = LEFT)
        
        #MOVING T'(0) BELOW OF T'(x)

        self.play(FadeIn(
            aprx_eq_deriv2,
            run_time = 2
        ))
        self.wait(7)

        #L4 REFACTORING T'(0)

        aprx_eq_deriv3 = TexMobject(r"\\0", "=", "b")
        aprx_eq_deriv3[0].set_color(PINK)
        aprx_eq_deriv3[2].set_color(RED)
        aprx_eq_deriv3.scale(0.8).next_to(aprx_eq_deriv2.get_part_by_tex("b"), DOWN, aligned_edge = RIGHT)

        #MOVING REFACTORED T'(0) BELOW T'(0)

        self.play(FadeIn(
            aprx_eq_deriv3,
            run_time = 2
        ))
        self.wait(2)

        #L1 NEW T(x)

        aprx_eq_new = TexMobject(r"\\T(x)", "=", "1", "+", "0", "x")
        aprx_eq_new[0].set_color(ORANGE)
        aprx_eq_new[2].set_color(YELLOW)
        aprx_eq_new[4].set_color(RED)

        #TRANSFORMING L1 
        
        aprx_eq_new.scale(0.8).next_to(aprx_eq_deriv.get_part_by_tex("T"), UP, aligned_edge = LEFT)
        self.play(Transform(
            aprx_eq,
            aprx_eq_new,
            run_time = 2
        ))
        self.wait()

        #GRAPHING SECOND APPROXIMATION TERM
        new_graph = self.get_graph(functools.partial(taylor_approximation_cos, 1), x_min = self.x_min, x_max = self.x_max).set_color(ORANGE)
        self.play(
            Transform(graph, new_graph, run_time=2),
        )
        self.wait(3)

        #FADING EVERYTHING OUT OF SCENE

        self.play(
            FadeOutAndShift(aprx_eq , direction=RIGHT),
            FadeOutAndShift(aprx_eq_deriv , direction=RIGHT),
            FadeOutAndShift(aprx_eq_deriv2, direction=RIGHT),
            FadeOutAndShift(aprx_eq_deriv3, direction=RIGHT),
        )
        self.remove(cos_eq, cos_deriv_1, l, f_eql_0, f_eql_1, sentence, graph)

    def third_approximation(self):

        ##################
        #ADDING THE GRAPH#
        ##################

        graph = self.get_graph(functools.partial(taylor_approximation_cos, 1), x_min = self.x_min, x_max = self.x_max).set_color(ORANGE)
        self.add(graph)

        #####################
        #LEFT SIDE OF SCREEN#
        #####################

        placeholder = TexMobject("f'''(x) = -sin(x)") #wird nicht verwendet, nur placeholder
        placeholder.scale(0.6).to_corner(UL)
        cos_eq = TexMobject("f(x) = cos(x)").set_color(BLUE)
        cos_eq.scale(0.6).next_to(placeholder, DOWN, aligned_edge = RIGHT).to_edge(LEFT)
        self.add(cos_eq)

        #Spaltentrennungslinie zeichnen
        l = Line(6*DOWN + RIGHT)
        l.next_to(placeholder)
        self.add(l)

        #bei x = 0 als zweite Spalte
        x_eql_0text = TextMobject("bei ")
        x_eql_0text.scale(0.6)
        x_eql_0 = TexMobject("x = 0")
        x_eql_0.scale(0.6)
        sentence=VGroup(x_eql_0text,x_eql_0)
        sentence.arrange_submobjects(RIGHT, buff=0.1).next_to(placeholder, RIGHT, buff = 0.5)
        self.add(sentence)
        #self.play(Write(x_eql_0text))
        #self.play(Write(x_eql_0))

        #cos is equal to 1
        f_eql_1 = TexMobject("1")
        f_eql_1.scale(0.6).next_to(cos_eq, RIGHT, buff = 1.55)
        self.add(f_eql_1)

        #cos derivative (sin) underneath cos
        cos_deriv_1 = TexMobject("f'(x) = -sin(x)")
        cos_deriv_1.scale(0.6)
        cos_deriv_1.next_to(cos_eq, DOWN).to_edge(LEFT)
        self.add(cos_deriv_1)

        #sin is equal to 0
        f_eql_0 = TexMobject("0")
        f_eql_0.scale(0.6).next_to(cos_deriv_1, RIGHT, buff = 1.22)
        self.add(f_eql_0)

        #NEW STUFF
        self.wait(20)
        #cos second derivative (-cos) underneath sin

        cos_deriv_2 = TexMobject("f''(x) = -cos(x)")
        cos_deriv_2.scale(0.6)
        cos_deriv_2.next_to(cos_deriv_1, DOWN).to_edge(LEFT)
        self.play(ReplacementTransform(cos_deriv_1.copy(), cos_deriv_2))

        #-cos is equal to -1
        self.wait(7)
        f_eql_n1 = TexMobject("-1")
        f_eql_n1.set_color(PINK)
        f_eql_n1.scale(0.6).next_to(cos_deriv_2, RIGHT, buff = 1)
        self.play(ReplacementTransform(cos_deriv_2.copy(), f_eql_n1))
        
        ######################
        #RIGHT SIDE OF SCREEN#
        ######################
        
        self.wait(3)
        #L1 creating T(x)
        aprx_eq = TexMobject(r"\\T(x)", "=", "1", "+", "0", "x", "+", "c", "x^{2}")
        aprx_eq[0].set_color(ORANGE)
        aprx_eq[2].set_color(YELLOW)
        aprx_eq[4].set_color(RED)
        aprx_eq[7].set_color(GREEN)


        #Moving the T(x) to the top left and show it
        
        aprx_eq.scale(0.8).to_corner(UR)
        self.play(Write(
            aprx_eq,
            run_time = 2
        ))
        self.wait(4)

        #SHOWING THE INFLUENCE b HAS ON THE GRAPH
        #CHANING INPUT b
        c = [0.8, -0.3, 1, 0.25, -0.9]
        for n in c:
            new_graph = self.get_graph(lambda x: 1+n*x**2, x_min = self.x_min, x_max = self.x_max).set_color(ORANGE)
            self.play(
                Transform(graph, new_graph, run_time=3),
            )
        
        self.wait(4)
        #L2 Derivative of T(x)
        
        aprx_eq_deriv = TexMobject(r"\\{T}'(x) =", "0", "+", "2", "c", "x",)
        aprx_eq_deriv[1].set_color(RED)
        aprx_eq_deriv[4].set_color(GREEN)
        aprx_eq_deriv.scale(0.8).next_to(aprx_eq.get_part_by_tex("T"), DOWN, aligned_edge = LEFT)

        #Transforming T(x) into T'(x)

        self.play(ReplacementTransform(aprx_eq.copy(), aprx_eq_deriv))
        self.wait()
        
        #L3 second Derivative of T(x)
        
        aprx_eq_deriv2 = TexMobject(r"\\{T}''(x) =", "2", "c")
        aprx_eq_deriv2[2].set_color(GREEN)
        aprx_eq_deriv2.scale(0.8).next_to(aprx_eq_deriv.get_part_by_tex("T"), DOWN, aligned_edge = LEFT)

        #Transforming T'(x) into T''(x)

        self.play(ReplacementTransform(aprx_eq_deriv.copy(), aprx_eq_deriv2))
        self.wait(17)

        #L4 T''(x) = -1
        
        aprx_eq_deriv3 = TexMobject("-1 ", "=", "2", "c")
        aprx_eq_deriv3[0].set_color(PINK)
        aprx_eq_deriv3[3].set_color(GREEN)
        aprx_eq_deriv3.scale(0.8).next_to(aprx_eq_deriv2.get_part_by_tex("c"), DOWN, aligned_edge = RIGHT)

        #Moving -1 = 2c underneath T''(x)

        self.play(FadeIn(aprx_eq_deriv3))
        self.wait(3)

        #L5 -1/2 = c

        aprx_eq_deriv4 = TexMobject("-", r"\frac{1}{2}", "=", "c")
        aprx_eq_deriv4[0].set_color(PINK) #- is pink
        aprx_eq_deriv4[1][0].set_color(PINK) #1 is pink
        aprx_eq_deriv4[3].set_color(GREEN)#c is green  
        aprx_eq_deriv4.scale(0.8).next_to(aprx_eq_deriv3, DOWN, )

        #MOVING -1/2 = c below -1 = 2c

        self.play(FadeIn(aprx_eq_deriv4))
        self.wait(2)

        #L1 NEW T(x)

        aprx_eq_new = TexMobject(r"\\T(x)", "=", "1", "-", r"\frac{1}{2}", "x^{2}")
        aprx_eq_new[0].set_color(ORANGE)
        aprx_eq_new[2].set_color(YELLOW)
        aprx_eq_new[3].set_color(GREEN)
        aprx_eq_new[4].set_color(GREEN)
        aprx_eq_new.scale(0.8).next_to(aprx_eq_deriv.get_part_by_tex("T"), UP, aligned_edge = LEFT)

        #TRANSFORMING L1 
        
        self.play(ReplacementTransform(
            aprx_eq,
            aprx_eq_new,
            run_time = 2
        ))
        self.wait(1)

        #GRAPHING THIRD APPROXIMATION TERM
        new_graph = self.get_graph(functools.partial(taylor_approximation_cos, 2), x_min = self.x_min, x_max = self.x_max).set_color(ORANGE)
        self.play(
            Transform(graph, new_graph, run_time=2),
        )
        self.wait(8)
        #FADING EVERYTHING OUT OF SCENE
        self.play(
            FadeOutAndShift(aprx_eq_deriv , direction=RIGHT),
            FadeOutAndShift(aprx_eq_deriv2, direction=RIGHT),
            FadeOutAndShift(aprx_eq_deriv3, direction=RIGHT),
            FadeOutAndShift(aprx_eq_deriv4, direction=RIGHT),
            FadeOutAndShift(cos_eq, direction = LEFT),
            FadeOutAndShift(cos_deriv_1, direction = LEFT),
            FadeOutAndShift(cos_deriv_2, direction = LEFT),
            FadeOutAndShift(l, direction = LEFT),
            FadeOutAndShift(f_eql_0, direction = LEFT),
            FadeOutAndShift(f_eql_1, direction = LEFT),
            FadeOutAndShift(f_eql_n1, direction = LEFT),
            FadeOutAndShift(sentence, direction = LEFT),
        )
        
        #MORE GRAPHS
        #2 TERMS
        aprx_eq = TexMobject("T(x)", "= 1 -", r"\frac{1}{2}", "x^{2}")
        aprx_eq[0].set_color(ORANGE)
        aprx_eq.scale(0.8).to_corner(UL)
        self.play(ReplacementTransform(aprx_eq_new, aprx_eq))
        self.wait()

        #3 TERMS
        third_term = TexMobject("T(x)", r"= 1 - \frac{1}{2}x^{2} + \frac{1}{24}x^{4}")
        third_term[0].set_color(ORANGE)
        third_term.scale(0.8).to_corner(UL)
        self.play(Write(third_term))
        new_graph = self.get_graph(functools.partial(taylor_approximation_cos, 3), x_min = self.x_min, x_max = self.x_max).set_color(ORANGE)
        self.play(
            Transform(graph, new_graph, run_time=2),
        )
        self.remove(aprx_eq)
        self.wait()

        #4 TERMS
        forth_term = TexMobject("T(x)", r"= 1 - \frac{1}{2}x^{2} + \frac{1}{24}x^{4} - \frac{1}{720}x^{6}")
        forth_term[0].set_color(ORANGE)
        forth_term.scale(0.8).to_corner(UL)
        self.play(Write(forth_term))
        new_graph = self.get_graph(functools.partial(taylor_approximation_cos, 4), x_min = self.x_min, x_max = self.x_max).set_color(ORANGE)
        self.play(
            Transform(graph, new_graph, run_time=2),
        )
        self.remove(third_term)
        self.wait()

        #5 TERMS
        fifth_term = TexMobject("T(x)", r"= 1 - \frac{1}{2}x^{2} + \frac{1}{24}x^{4} - \frac{1}{720}x^{6} + \frac{1}{40320}x^{8}")
        fifth_term[0].set_color(ORANGE)
        fifth_term.scale(0.8).to_corner(UL)
        self.play(Write(fifth_term))
        new_graph = self.get_graph(functools.partial(taylor_approximation_cos, 5), x_min = self.x_min, x_max = self.x_max).set_color(ORANGE)
        self.play(
            Transform(graph, new_graph, run_time=2),
        )
        self.remove(forth_term)
        self.wait()

        #6 TERMS
        sixth_term = TexMobject("T(x)", r"= 1 - \frac{1}{2}x^{2} + \frac{1}{24}x^{4} - \frac{1}{720}x^{6} + \frac{1}{40320}x^{8} - \frac{1}{3628800} x^{10}")
        sixth_term[0].set_color(ORANGE)
        sixth_term.scale(0.8).to_corner(UL)
        self.play(Write(sixth_term))
        new_graph = self.get_graph(functools.partial(taylor_approximation_cos, 6), x_min = self.x_min, x_max = self.x_max).set_color(ORANGE)
        self.play(
            Transform(graph, new_graph, run_time=2),
        )
        self.remove(fifth_term)
        self.wait(3)

        #transforming to factorials
        eq_w_fac_coloured = TexMobject("T(x)", "= ", "+", r"\frac{1}{0!}x^{0}", "-", r"\frac{1}{2!}x^{2}", "+", r"\frac{1}{4!}x^{4}", "-", r"\frac{1}{6!}x^{6}", "+", r"\frac{1}{8!}x^{8}", "-", r"\frac{1}{10!}x^{10}")
        eq_w_fac_coloured[0].set_color(ORANGE)
        eq_w_fac_coloured.scale(0.8).to_corner(UL)
        self.play(ReplacementTransform(sixth_term, eq_w_fac_coloured))

        #REMINDER
        self.wait(15)
        #first approx
        same_value = TexMobject("T(0)", "=", "f(0)", "=a=1")
        same_value[0].set_color(ORANGE)
        same_value[2].set_color(BLUE)
        same_value.scale(0.8).next_to(eq_w_fac_coloured.get_part_by_tex("T"), DOWN, aligned_edge = LEFT, buff = 0.3)
        self.play(FadeIn(same_value))
        self.wait(10)

        #second approx
        same_fd = TexMobject("T'(0)", "=", "f'(0)", "=b=0")
        same_fd[0].set_color(ORANGE)
        same_fd[2].set_color(BLUE)
        same_fd.scale(0.8).next_to(same_value.get_part_by_tex("T"), DOWN, aligned_edge = LEFT)
        self.play(FadeIn(same_fd))
        self.wait(10)

        #third approx
        same_sd = TexMobject("T''(0)", "=", "f''(0)", "=2c=-1")
        same_sd[0].set_color(ORANGE)
        same_sd[2].set_color(BLUE)
        same_sd.scale(0.8).next_to(same_fd.get_part_by_tex("T"), DOWN, aligned_edge = LEFT)
        self.play(FadeIn(same_sd))
        self.wait(12)

        self.play(
            FadeOut(same_value, direction = LEFT),
            FadeOut(same_fd, direction = LEFT),
            FadeOut(same_sd, direction = LEFT),
        )
        self.wait(4)

        #first, second deriv x^10
        gx = TexMobject("g(x) = x^{10}").next_to(eq_w_fac_coloured.get_part_by_tex("T"), DOWN, aligned_edge = LEFT, buff = 0.3)
        gx_fd = TexMobject("g'(x) = 10x^{9}").scale(0.8).next_to(gx.get_part_by_tex("g"), DOWN, aligned_edge = LEFT)
        gx_sd = TexMobject("g''(x) = 90x^{8}").scale(0.8).next_to(gx_fd.get_part_by_tex("g"), DOWN, aligned_edge = LEFT)
        gx_td = TexMobject("g^{(10)}(x) = 10!").scale(0.8).next_to(gx_sd.get_part_by_tex("g"), DOWN, aligned_edge = LEFT)
        nx = TexMobject(r"h(x) = \frac{a \cdot x^n}{n!}").scale(0.8).next_to(gx_fd, RIGHT, aligned_edge = LEFT, buff = 0.6)
        nx_nd = TexMobject("h^{(n)}(x) = a").scale(0.8).next_to(nx.get_part_by_tex("h"), DOWN, aligned_edge = LEFT)

        self.play(FadeIn(gx))
        self.wait(2)
        self.play(ReplacementTransform(gx.copy(), gx_fd))
        self.wait(2)
        self.play(ReplacementTransform(gx_fd.copy(), gx_sd))
        self.wait(5)
        self.play(FadeIn(gx_td))
        self.wait(7)
        self.play(FadeIn(nx))
        self.wait(2)
        self.play(ReplacementTransform(nx.copy(), nx_nd))

        self.play(
            FadeOut(gx, direction = LEFT),
            FadeOut(gx_fd, direction = LEFT),
            FadeOut(gx_sd, direction = LEFT),
            FadeOut(gx_td, direction = LEFT)
        )

        self.wait(2)

        #COSINE FIRST SECOND THIRD FORTH DERIV

        cos = TexMobject("f(0) = cos(0) = 1").next_to(eq_w_fac_coloured.get_part_by_tex("T"), DOWN, aligned_edge = LEFT, buff = 0.3)
        nsin = TexMobject("f'(0) = -sin(0) = 0").scale(0.8).next_to(cos.get_part_by_tex("f"), DOWN, aligned_edge = LEFT)
        ncos = TexMobject("f''(0) = -cos(0) = -1").scale(0.8).next_to(nsin.get_part_by_tex("f"), DOWN, aligned_edge = LEFT)
        sin = TexMobject("f'''(0) = sin(0) = 0").scale(0.8).next_to(ncos.get_part_by_tex("f"), DOWN, aligned_edge = LEFT)

        self.play(FadeIn(cos))
        self.wait(3)
        self.play(ReplacementTransform(cos.copy(), nsin))
        self.wait(3)
        self.play(ReplacementTransform(nsin.copy(), ncos))
        self.wait(3)
        self.play(ReplacementTransform(ncos.copy(), sin))
        self.wait(15)

        #gerade
        cos.set_color(YELLOW)
        ncos.set_color(YELLOW)
        self.wait(3)
        for i in range(2,13,2):
            eq_w_fac_coloured[i].set_color(YELLOW)
            eq_w_fac_coloured[i+1].set_color(YELLOW)
            self.wait(2)
            eq_w_fac_coloured[i].set_color(WHITE)
            eq_w_fac_coloured[i+1].set_color(WHITE)
        #ungerade
        self.wait(3)
        cos.set_color(WHITE)
        ncos.set_color(WHITE)
        sin.set_color(RED)
        nsin.set_color(RED)
        self.wait(7)

        #colouring the + and - signs in green and red

        #eq_w_fac_coloured[2].set_color(GREEN)
        #eq_w_fac_coloured[4].set_color(RED)
        #eq_w_fac_coloured[6].set_color(GREEN)
        #eq_w_fac_coloured[8].set_color(RED)
        #eq_w_fac_coloured[10].set_color(GREEN)
        #eq_w_fac_coloured[12].set_color(RED)
        #cos[0][-1].set_color(GREEN)
        #ncos[0][-2].set_color(RED)
        #ncos[0][-1].set_color(RED)

        self.wait()

        self.play(
            FadeOut(cos, direction = LEFT),
            FadeOut(nsin, direction = LEFT),
            FadeOut(ncos, direction = LEFT),
            FadeOut(sin, direction = LEFT)
        )

        #Index Line
        index_I = TextMobject("Index ")
        index_I.scale(0.6)
        index_k = TexMobject("k:")
        index_k.scale(0.6)
        index = VGroup(index_I, index_k)
        index.arrange_submobjects(RIGHT, buff=0.1).to_corner(UL)
        eq_np = TexMobject("T(x) ", "= ", "+", r"\frac{1}{0!}x^{0}", "-", r"\frac{1}{2!}x^{2}", "+", r"\frac{1}{4!}x^{4}", "-", r"\frac{1}{6!}x^{6}", "+", r"\frac{1}{8!}x^{8}", "-", r"\frac{1}{10!}x^{10}").scale(0.8)
        eq_np[0].set_color(ORANGE)
        eq_np.next_to(index_I.get_part_by_tex("I"), DOWN, buff = 0.3, aligned_edge = LEFT)
        self.play(Transform(eq_w_fac_coloured, eq_np))
        self.play(Write(index))
        zero = TexMobject("0").scale(0.6)
        one = TexMobject("1").scale(0.6)
        two = TexMobject("2").scale(0.6)
        three = TexMobject("3").scale(0.6)
        four = TexMobject("4").scale(0.6)
        five = TexMobject("5").scale(0.6)
        indices = VGroup(zero, one, two, three, four, five)
        indices.arrange_submobjects(RIGHT, buff=1.2).next_to(index_k, RIGHT, buff = 0.7)
        self.play(Write(indices))
        txt_1 = TextMobject("Vorzeichen: ").scale(0.8)
        
        braces = Brace(eq_w_fac_coloured[2:4])
        txt_2 = TexMobject(r"(-1)^{0}").scale(0.8)
        brace_text=VGroup(txt_1,txt_2)
        brace_text.arrange_submobjects(RIGHT, buff=0.1).next_to(braces, DOWN)
        a0 = Arrow(zero, eq_w_fac_coloured[3][5], buff = 0.05).set_color(YELLOW)
        self.play(Write(braces))
        self.play(Write(brace_text))
        self.play(Write(a0))
        self.wait(2)

        braces2 = Brace(eq_w_fac_coloured[4:6])
        txt_1 = TextMobject("Vorzeichen:  ").scale(0.8)
        txt_2 = TexMobject(r"(-1)^{1}").scale(0.8)
        brace_text2=VGroup(txt_1,txt_2)
        brace_text2.arrange_submobjects(RIGHT, buff=0.1).next_to(braces2, DOWN)
        a1 = Arrow(one, eq_w_fac_coloured[5][5], buff = 0.05).set_color(YELLOW)
        self.play(
            Transform(braces, braces2),
            Transform(brace_text, brace_text2),
            Write(a1))
        self.wait(2)

        braces2 = Brace(eq_w_fac_coloured[6:8])
        txt_1 = TextMobject("Vorzeichen: ").scale(0.8)
        txt_2 = TexMobject(r"(-1)^{2}").scale(0.8)
        brace_text2=VGroup(txt_1,txt_2)
        brace_text2.arrange_submobjects(RIGHT, buff=0.1).next_to(braces2, DOWN)
        a2 = Arrow(two, eq_w_fac_coloured[7][5], buff = 0.05).set_color(YELLOW)
        self.play(
            Transform(braces, braces2),
            Transform(brace_text, brace_text2),
            Write(a2))
        self.wait(2)

        braces2 = Brace(eq_w_fac_coloured[8:10])
        txt_1 = TextMobject("Vorzeichen:  ").scale(0.8)
        txt_2 = TexMobject(r"(-1)^{3}").scale(0.8)
        brace_text2=VGroup(txt_1,txt_2)
        brace_text2.arrange_submobjects(RIGHT, buff=0.1).next_to(braces2, DOWN)
        a3 = Arrow(three, eq_w_fac_coloured[9][5], buff = 0.05).set_color(YELLOW)
        self.play(
            Transform(braces, braces2),
            Transform(brace_text, brace_text2),
            Write(a3))
        self.wait(2)

        braces2 = Brace(eq_w_fac_coloured[10:12])
        txt_1 = TextMobject("Vorzeichen: ").scale(0.8)
        txt_2 = TexMobject(r"(-1)^{4}").scale(0.8)
        brace_text2=VGroup(txt_1,txt_2)
        brace_text2.arrange_submobjects(RIGHT, buff=0.1).next_to(braces2, DOWN)
        a4 = Arrow(four, eq_w_fac_coloured[11][5], buff = 0.05).set_color(YELLOW)
        self.play(
            Transform(braces, braces2),
            Transform(brace_text, brace_text2),
            Write(a4))
        self.wait(2)

        braces2 = Brace(eq_w_fac_coloured[12:14])
        txt_1 = TextMobject("Vorzeichen:  ").scale(0.8)
        txt_2 = TexMobject(r"(-1)^{5}").scale(0.8)
        brace_text2=VGroup(txt_1,txt_2)
        brace_text2.arrange_submobjects(RIGHT, buff=0.1).next_to(braces2, DOWN)
        a5 = Arrow(five, eq_w_fac_coloured[13][6], buff = 0.05).set_color(YELLOW)
        self.play(
            Transform(braces, braces2),
            Transform(brace_text, brace_text2),
            Write(a5))
        
        self.wait(18)
        
        #Fading out braces and indices

        self.play(
            FadeOut(braces),
            FadeOut(brace_text),
            FadeOut(indices),
            FadeOut(index),
            FadeOut(a0),
            FadeOut(a1),
            FadeOut(a2),
            FadeOut(a3),
            FadeOut(a4),
            FadeOut(a5)
        )

        #EQ BEFORE SUM

        eq_before_sum = TexMobject("T(x)", r"=(-1)^{0}\cdot \frac{x^{2\cdot 0}}{(2\cdot 0)!}", r"+(-1)^{1}\cdot \frac{x^{2\cdot 1}}{(2\cdot 1)!}", r"+(-1)^{2}\cdot \frac{x^{2\cdot 2}}{(2\cdot 2)!}", r"+(-1)^{3}\cdot \frac{x^{2\cdot 3}}{(2\cdot 3)!}", r"+(-1)^{4}\cdot \frac{x^{2\cdot 4}}{(2\cdot 4)!}", r"+(-1)^{5}\cdot \frac{x^{2\cdot 5}}{(2\cdot 5)!}")
        eq_before_sum[0].set_color(ORANGE)
        eq_before_sum.scale(0.55).to_corner(UL)

        #colouring the whole equation before combining to a sum
        eq_before_sum[1][5].set_color(BLUE)
        eq_before_sum[1][10].set_color(BLUE)
        eq_before_sum[1][15].set_color(BLUE)
        eq_before_sum[2][5].set_color(TEAL)
        eq_before_sum[2][10].set_color(TEAL)
        eq_before_sum[2][15].set_color(TEAL)
        eq_before_sum[3][5].set_color(YELLOW)
        eq_before_sum[3][10].set_color(YELLOW)
        eq_before_sum[3][15].set_color(YELLOW)
        eq_before_sum[4][5].set_color(GOLD)
        eq_before_sum[4][10].set_color(GOLD)
        eq_before_sum[4][15].set_color(GOLD)
        eq_before_sum[5][5].set_color(RED)
        eq_before_sum[5][10].set_color(RED)
        eq_before_sum[5][15].set_color(RED)
        eq_before_sum[6][5].set_color(MAROON)
        eq_before_sum[6][10].set_color(MAROON)
        eq_before_sum[6][15].set_color(MAROON)

        eq_before_sum[1][2].set_color(PINK)
        eq_before_sum[1][3].set_color(PINK)
        eq_before_sum[1][7].set_color(PINK)
        eq_before_sum[1][8].set_color(PINK)
        eq_before_sum[1][13].set_color(PINK)
        for i in range(2, 7):
            eq_before_sum[i][2].set_color(PINK)
            eq_before_sum[i][3].set_color(PINK)
            eq_before_sum[i][7].set_color(PINK)
            eq_before_sum[i][8].set_color(PINK)
            eq_before_sum[i][13].set_color(PINK)

        self.play(ReplacementTransform(eq_w_fac_coloured, eq_before_sum))
        
        self.wait(35)
        eq_as_sum = TexMobject("T(x)", r"= \sum_{k=0}^{5}\left(-1\right)^{k}\cdot\frac{x^{2k}}{\left(2k\right)!}")
        eq_as_sum[0].set_color(ORANGE)
        eq_as_sum.to_corner(UL)
        self.play(ReplacementTransform(eq_before_sum, eq_as_sum))
        self.wait(2)
        self.play(FadeOut(VGroup(*self.mobjects)))

class SqrtTask(Scene):

    def construct(self):
        #Gleichungsumformungen
        equation_1 = TexMobject(r"\int_{0}^{1}x\cdot\sqrt{x\cdot\sqrt[3]{x\cdot\sqrt[4]{x\cdot\sqrt[5]{\cdots}}}}dx").scale(0.8).to_corner(UL)
        equation_2 = TexMobject (r"\int_{0}^{1}x^{1}\cdot x^{\frac{1}{2}}\cdot x^{\frac{1}{2\cdot3}}\cdot x^{\frac{1}{2\cdot3\cdot4}}\cdot \cdots dx").scale(0.8).next_to(equation_1, direction = DOWN, aligned_edge = LEFT)
        equation_3 = TexMobject (r"\int_{0}^{1}x^{\frac{1}{1}+\frac{1}{2}+\frac{1}{2\cdot3}+\frac{1}{2\cdot3\cdot4}+\cdots}dx").next_to(equation_2, direction = DOWN, aligned_edge = LEFT)
        equation_4 = TexMobject (r"\int_{0}^{1}x^{\frac{1}{1!}+\frac{1}{2!}+\frac{1}{3!}+\frac{1}{4!}+...+\frac{1}{0!}-\frac{1}{0!}}dx").next_to(equation_3, direction = DOWN, aligned_edge = LEFT)
        equation_5 = TexMobject (r"\int_{0}^{1}x^{\sum_{n=0}^{\infty}\left(\frac{1}{n!}\right)-1}dx").scale(0.8).to_corner(UR).to_edge(RIGHT, buff = 1)
        equation_6 = TexMobject (r"\int_{0}^{1}x^{e-1}dx").scale(0.8).next_to(equation_5, direction = DOWN, aligned_edge = LEFT)
        equation_7 = TexMobject (r"\left[\frac{x^{e}}{e}\right]_0^1").scale(0.8).next_to(equation_6, direction = DOWN, aligned_edge = LEFT)
        equation_8 = TexMobject (r"\left(\frac{1^{e}}{e}\right)  - \left(\frac{0^{e}}{e}\right)").scale(0.8).next_to(equation_7, direction = DOWN, aligned_edge = LEFT)
        equation_9 = TexMobject (r"\frac{1}{e}").scale(0.8).next_to(equation_8, direction = DOWN, aligned_edge = LEFT)
        
        #Erinnerungen und Nebenrechnungen
        text = TextMobject("Nebenrechnungen:").to_corner(UR)
        reminder_1 = TexMobject (r"\sqrt{a \cdot b} = \sqrt{a} \cdot \sqrt{b}").scale(0.8).next_to(text, direction = DOWN, aligned_edge = LEFT, buff = 0.6)
        reminder_2 = TexMobject ( r"\sqrt[c] {\sqrt[d]{a}} = \sqrt[c \cdot d] {a}").scale(0.8).next_to(reminder_1, direction = DOWN, aligned_edge = LEFT)
        reminder_3 = TexMobject ( r"\sqrt{a \cdot \sqrt[3]{b}} = \sqrt {a} \cdot \sqrt[2 \cdot 3]{b}").scale(0.8).next_to(reminder_2, direction = DOWN, aligned_edge = LEFT)
        
        self.wait(2)
        self.play(Write(equation_1))
        self.wait(2)
        self.play(Write(text))
        self.wait(2)
        self.play(Write(reminder_1))
        self.wait(2)
        self.play(Write(reminder_2))
        self.wait(2)
        self.play(
            ReplacementTransform(reminder_1.copy(), reminder_3),
            ReplacementTransform(reminder_2.copy(), reminder_3)
        )
        self.wait(2)
        self.play(Write(equation_2))
        self.wait(2)
        self.play(Write(equation_3))
        self.wait(2)
        self.play(Write(equation_4))
        self.wait(2)
        self.play(
            FadeOutAndShift(text, direction = RIGHT),
            FadeOutAndShift(reminder_1, direction = RIGHT),
            FadeOutAndShift(reminder_2, direction = RIGHT),
            FadeOutAndShift(reminder_3, direction = RIGHT)
        )
        self.play(Write(equation_5))
        self.wait(2)
        self.play(Write(equation_6))
        self.wait(2)
        self.play(Write(equation_7))
        self.wait(2)
        self.play(Write(equation_8))
        self.wait(2)
        self.play(Write(equation_9))
        self.wait(2)
        self.play(FadeOut(VGroup(*self.mobjects)))
        self.wait(2)

class NewtonVerfahren(GraphScene):
    CONFIG = {
        "x_min" : -2,
        "x_max" : 4,
        #"x_tick_frequency" : 0,
        "x_axis_label": "$x$",
        #"x_labeled_nums": np.arange(-5,3,1),
        "y_min" : -2,
        "y_max" : 3,
        "y_axis_width": 1,
        #"y_tick_frequency" : 1, 
        "y_axis_label": "$y$",
        #"y_labeled_nums": np.arange(-1,7,1),
        "graph_origin": 4*LEFT + 0.5*DOWN, 
        #"graph_origin": ORIGIN, 
    }
    
    def construct(self):
        self.wait(2)
        self.setup_axes(animate = True)

        #die Funktion, deren Nullstelle wir nicht berechnen können.
        def func(x):
            return ((x**2-1-x**0.5+x*math.pow(math.cos(x),2)+(x-1.5)**3)/(x+5)+0.3)
        graph = self.get_graph(func, x_min = 0.01)
        self.play(ShowCreation(graph))
        self.wait()

        x_v = 3 #Startwert des Newton Verfahren
        value = 1 #value braucht ein Wert, damit die while schleife anfängt

        #Definition den Punktes und in Ursprung des Graphen
        dot = Dot()
        dot.move_to(self.coords_to_point(0,0)).set_color(RED)
        next_line = Line()

        #Punkt in den Vordergrund, damit immer vor den Graphen
        self.foreground_mobjects.append(dot)

        #die Indize von p als Array, da aufgrund von "LaTeX Error: Converting to DVI" man nicht mit variable schreiben kann
        ps = [TexMobject(r"p_{1}"), TexMobject(r"p_{2}"), TexMobject(r"p_{3}"), TexMobject(r"p_{4}"), TexMobject(r"p_{5}"), 
            TexMobject(r"p_{6}"), TexMobject(r"p_{7}"), TexMobject(r"p_{8}"), TexMobject(r"p_{9}"), TexMobject(r"p_{10}"), ]
        ps_2 = [TexMobject(r"p_{1}"), TexMobject(r"p_{2}"), TexMobject(r"p_{3}"), TexMobject(r"p_{4}"), TexMobject(r"p_{5}"), 
            TexMobject(r"p_{6}"), TexMobject(r"p_{7}"), TexMobject(r"p_{8}"), TexMobject(r"p_{9}"), TexMobject(r"p_{10}"), ]
        ps_3 = [TexMobject(r"p_{1}"), TexMobject(r"p_{2}"), TexMobject(r"p_{3}"), TexMobject(r"p_{4}"), TexMobject(r"p_{5}"), 
            TexMobject(r"p_{6}"), TexMobject(r"p_{7}"), TexMobject(r"p_{8}"), TexMobject(r"p_{9}"), TexMobject(r"p_{10}"), ]
        
        #Schleife läuft so lange, bis das Newton Verfahren eine Abweichung unter 0.001 hat
        number_of_approximations = 0
        while abs(value) > 0.001:
            #Newton y wert ist func an newton x Wert
            y_v = func(x_v)

            #Graph der Tangente mit Breite 5
            tan_line = Line(*[
                self.coords_to_point(x_v+x,func(x_v)+derivative(func,x_v)*x)
                for x in (-2.5,2.5)
                ]).set_color(YELLOW)

            #Linie von Tangentenpunkt zur x-achse
            if value == 1:
                line_point_to_x_axis = Line(*[
                    self.coords_to_point(x_v, y)
                    for y in (0, y_v)
                ]).set_color(GREY_BROWN)
            else:
                line_point_to_x_axis = next_line.copy()
            
            p = ps[number_of_approximations]
            p.scale(0.6).next_to(line_point_to_x_axis, DOWN).add_background_rectangle(buff = 0.1)

            #Tangenten Gleichung zur Nullstellen Berechnung
            def tan_func(x):
                return (func(x_v)+(x-x_v)*derivative(func,x_v))

            #Moving dot
            if value == 1:
                self.play(GrowFromCenter(line_point_to_x_axis))
            else:
                self.add(line_point_to_x_axis)
                self.remove(next_line)
            self.play(FadeIn(p), run_time = 0.5)
            self.play(dot.move_to, self.coords_to_point(x_v, y_v))            

            #calculate value and add the string
            value = func(x_v)
            value_str = str(round(value, 6))
            aprx_zero_x = VGroup(ps_2[number_of_approximations],TexMobject("=",str(round(x_v,7)))).arrange_submobjects(RIGHT, buff = 0.05).scale(0.6).to_corner(UL)
            current_value = VGroup(TexMobject(r"f("), ps_3[number_of_approximations], TexMobject(r")\approx", value_str)).arrange_submobjects(RIGHT, buff = 0.05).scale(0.6).to_corner(UL).shift(DOWN)
            if(x_v != 3):
                self.play(
                    Transform(x_string, aprx_zero_x),
                    Transform(value_string, current_value)
                )
            else:
                x_string = aprx_zero_x
                value_string = current_value
                self.play(
                    Write(x_string),
                    Write(value_string)
                )
            
            #aniamte tangent line
            self.play(GrowFromCenter(tan_line))

            #calculate new zero for the next line
            x_v = nullstelle_linear(tan_func)

            self.wait(2)
            if abs(value) > 0.001:
                #next line
                next_line = Line(*[
                    self.coords_to_point(x_v, y)
                    for y in (0, func(x_v))
                ]).set_color(GREY_BROWN)
                self.play(GrowFromCenter(next_line))
                self.wait(1)
                self.play(
                    FadeOut(tan_line, run_time = 0.5),
                    FadeOut(line_point_to_x_axis, run_time = 0.5),
                    FadeOut(p, run_time = 0.5),    
                )
    
            number_of_approximations += 1
            

        self.wait(3)
        self.play(FadeOut(VGroup(*self.mobjects)))
        
class CompleteForm(GraphScene):
    CONFIG={
        "x_min": -8,
        "x_max": 8,
        "x_axis_width": 13,
        "x_tick_frequency": 2,
        "x_labeled_nums": np.arange(-8,10,2),
        "y_min": -2,
        "y_max": 20,
        "y_tick_frequency": 5,
        "y_labeled_nums": np.arange(0,21,5),
        "graph_origin": 2*DOWN,
   }

    def construct(self):
        self.wait(30)
        first_l1 = TextMobject("1: Werte der Ableitungen des Polynom")
        first_l2 = TextMobject("und der Funktion sollen identisch sein")
        first = VGroup(first_l1, first_l2)
        first.arrange_submobjects(DOWN, buff = 0.15, aligned_edge = LEFT).to_corner(UL)
        second = TextMobject("2: Polynomreihe mit unendlich Termen").to_corner(UL).next_to(first, DOWN, buff = 0.4, aligned_edge = LEFT)
        third_l1 = TextMobject("3: Jeder Term repräsentiert den Wert")
        third_l2 = TextMobject("einer höheren Ableitung")
        third = VGroup(third_l1, third_l2)
        third.arrange_submobjects(DOWN, buff = 0.15, aligned_edge = LEFT).next_to(second, DOWN, buff = 0.4, aligned_edge = LEFT)
        reminder = TexMobject(r"f(x) = \frac{c\cdot x^{n}}{n!}").to_corner(UR)
        reminder_2 = TexMobject(r"f^{\left(n\right)}\left(x\right)=c").next_to(reminder, DOWN, aligned_edge = LEFT)
        t_sum = TexMobject(r"T(x) = \sum_{n=0}^{k}").move_to(DOWN + 1.98*LEFT)
        #n_te = TextMobject("Wert der n-ten Ableitung").move_to(0.92*DOWN + -0.61*RIGHT, aligned_edge = LEFT)
        #n_te_deriv = TexMobject(r"f^{\left(n\right)}\left(0\right)").move_to(0.92*DOWN + -0.61*RIGHT, aligned_edge = LEFT)
        n_te_deriv_poly = TexMobject(r"\frac{f^{\left(n\right)}\left(0\right)}{n!}\cdot")
        x_to_n = TexMobject(r"x^{n}").next_to(n_te_deriv_poly)
        wtf = VGroup(n_te_deriv_poly, x_to_n)
        wtf.arrange_submobjects(RIGHT, buff = 0.2).move_to(0.92*DOWN + -0.61*RIGHT, aligned_edge = LEFT)
        full_taylor_1 = TexMobject(r"\left(x-a\right)^{n}").next_to(t_sum, buff = 2.2)
        full_taylor_2 = TexMobject(r"\frac{f^{\left(n\right)}\left(a\right)}{n!}\cdot ").move_to(0.92*DOWN + -0.61*RIGHT, aligned_edge = LEFT)
        #full_taylor = TexMobject(r"T(x) = \sum_{n=0}^{k}\frac{f^{\left(n\right)}\left(a\right)}{n!}\cdot\left(x-a\right)^{n}").move_to(DOWN)
        self.play(Write(first, run_time = 4))
        self.wait(5)
        self.play(Write(second, run_time = 2))
        self.wait(5)
        self.play(Write(third, run_time = 4))
        self.wait(10)
        #self.play(Write(t_sum), Write(n_te))
        #self.wait()
        self.play(Write(reminder))
        self.wait(4)
        self.play(Write(reminder_2))
        self.wait(15)
        self.play(Write(t_sum))
        self.play(Write(wtf))
        self.wait(5)
        everything = VGroup(*self.mobjects)
        self.play(everything.shift, 14*LEFT)
        #X^2 EXAMPLE
        self.wait(3)
        self.setup_axes(animate = True)
        f = self.get_graph(lambda x: math.pow(x,2))
        formula_1 = TexMobject(r"f(x) =")
        formula_2 = TexMobject(r"x^{2}").next_to(formula_1)
        formula = VGroup(formula_1, formula_2).arrange_submobjects(RIGHT, buff = 0.2).to_corner(UR).shift(DOWN + 1.5*LEFT)

        self.play(ShowCreation(f))
        self.play(Write(formula))
        self.wait()
        formula_2 = TexMobject(r"(x-2)^{2}").next_to(formula_1)
        f_2 = self.get_graph(lambda x: math.pow(x-2,2))
        self.play(
            ReplacementTransform(f,f_2),
            ReplacementTransform(formula[1], formula_2),
        )
        self.wait(5)
        self.play(VGroup(*self.mobjects).shift, 14*RIGHT)
        #BACK TO OLD STUFF
        self.wait(5)
        self.play(ReplacementTransform(wtf[-1], full_taylor_1), ReplacementTransform(wtf[0], full_taylor_2))
        self.wait(5)
        self.play(FadeOut(VGroup(*self.mobjects)))

class AddOnGraph_1(GraphScene):
    CONFIG={
        "x_min": -8,
        "x_max": 8,
        "x_axis_width": 13,
        "x_tick_frequency": 2,
        "x_labeled_nums": np.arange(-8,10,2),
        "y_min": -2,
        "y_max": 20,
        "y_tick_frequency": 5,
        "y_labeled_nums": np.arange(0,21,5),
        "graph_origin": 2*DOWN,
    }
    def setup(self):
        GraphScene.setup(self)
    
    def construct(self):
        self.wait(5)
        self.setup_axes(animate = True)
        f = self.get_graph(lambda x: math.pow(x,2))
        formula_1 = TexMobject(r"f(x) =")
        formula_2 = TexMobject(r"x^{2}").next_to(formula_1)
        formula = VGroup(formula_1, formula_2).arrange_submobjects(RIGHT, buff = 0.2).to_corner(UR).shift(DOWN + 1.5*LEFT)

        self.play(ShowCreation(f))
        self.play(Write(formula))
        self.wait()
        formula_2 = TexMobject(r"(x-2)^{2}").next_to(formula_1)
        f_2 = self.get_graph(lambda x: math.pow(x-2,2))
        self.play(
            ReplacementTransform(f,f_2),
            ReplacementTransform(formula[1], formula_2),
        )
        self.wait(5)

class AddOnGraph_2(GraphScene):
    CONFIG={
        "x_min" : -2*np.pi,
        "x_max" : 2*np.pi,
        "x_tick_frequency" : np.pi/2,
        "x_axis_label": "$x$",
        "x_axis_width": 13,
        #"x_labeled_nums": np.arange(-8,10,2),
        "y_min" : -2,
        "y_max" : 2,
        "y_tick_frequency" : 1, 
        #"y_axis_label": "$f(x)$",
        #"y_labeled_nums": np.arange(-4,5,1),
        "graph_origin": 1*DOWN,
    }
    def setup(self):
        GraphScene.setup(self)
    
    def construct(self):
        self.wait(1)
        self.setup_axes(animate = True)
        cos = self.get_graph(lambda x: math.sin(x)).set_color(BLUE)
        formula = TexMobject("T(x) = 0" ).to_corner(UL).set_color(GREEN)
        appSin = TexMobject(r"\approx", r"sin\left(x\right)").next_to(formula, RIGHT)
        appSin[-1].set_color(BLUE)
        at = TextMobject("Nahe x = 0").next_to(appSin, RIGHT, buff = 0.6)
        formula_2 = TexMobject(r"+1 \cdot x").next_to(formula, RIGHT).set_color(GREEN)
        formula_3 = TexMobject(r"+0 \cdot x^{2}").next_to(formula_2, RIGHT).set_color(GREEN).shift(0.05*UP)
        formula_4 = TexMobject(r"-\frac{1}{3!} \cdot x^{3}").next_to(formula_3).set_color(GREEN).shift(0.05*DOWN)
        sAp = self.get_graph(lambda x: 0).set_color(GREEN)
        sAp_2 = self.get_graph(lambda x: x).set_color(GREEN)
        sAp_3 = self.get_graph(lambda x: x).set_color(GREEN)
        sAp_4 = self.get_graph(lambda x: x- math.pow(x,3)/6).set_color(GREEN)
        self.play(ShowCreation(cos), run_time = 2)
        self.play(
            ShowCreation(sAp, run_time = 2),
            Write(formula),
            Write(appSin)
        )
        self.wait(2)
        self.play(
            Transform(sAp, sAp_2, run_time = 2),
            Write(formula_2),
            appSin.shift, 1.6*RIGHT,
            at.shift, 1.6*RIGHT
        )
        self.wait(8)
        self.play(
            Transform(sAp, sAp_3, run_time = 2),
            Write(formula_3),
            appSin.shift, 1.6*RIGHT,
            at.shift, 1.6*RIGHT
        )
        self.wait(2)
        self.play(
            Transform(sAp, sAp_4, run_time = 2),
            Write(formula_4),
            appSin.shift, 1.9*RIGHT,
            at.shift, 1.9*RIGHT
        )
        self.wait(5)
        self.play(VGroup(*self.mobjects).shift, 14*LEFT)

def nullstelle_linear(func):
    value = -func(0)    #-, da bei Umformung zur Nullstelle - benötigt ist
    deriv = derivative(func, 0)
    return (value/deriv)

#n-te Ableitung einer Funktion an Stelle x mit dx von 0.01
def derivative(func, x, order=1, dx = 0.01):        #Wenn nichts anderes angegeben, wird die erste Ableitung mit dx = 0.01 zurückgegeben
    partial = [func(x + (i - order/2)*dx) for i in range(order+1)]
    while(len(partial) > 1):
        partial = [
            (partial[j+1] - partial[j])/dx
            for j in range(len(partial)-1)
        ]
    return(partial[0])

#Taylor Annäherung einer Funktion mit k Termen an Entwicklungsstelle a
def taylor_approximation(func, term_count, center_point = 0):
    coefficients = [
        derivative(func, center_point,n)/math.factorial(n)
        for n in range(term_count +1)
    ]
    return lambda x: sum([
        coefficients[n]*(x-center_point)**n
        for n in range(term_count +1)
    ])

class expApproximation(GraphScene):
    CONFIG = {
        "x_min" : -6,
        "x_max" : 4,
        "x_tick_frequency" : 1,
        "x_axis_label": "$x$",
        #"x_labeled_nums": np.arange(-5,3,1),
        "y_min" : -1,
        "y_max" : 20,
        "y_tick_frequency" : 1, 
        "y_axis_label": "$y$",
        #"y_labeled_nums": np.arange(-1,7,1),
        "graph_origin": 1*RIGHT + 2*DOWN, 
        #"graph_origin": ORIGIN, 
    }

    def setup(self):            
        GraphScene.setup(self)

    def construct(self):
        self.setup_axes(animate=True)
        def exp_func(x):
            return math.exp(x)

        exp_graph = self.get_graph(exp_func, x_min = self.x_min, x_max = self.x_max)
        exp_graph.set_color(BLUE)

        self.play(
            ShowCreation(exp_graph), run_time = 3
        )
        self.wait(2)

        #EXP AND ITS DERIVATIVES
        eq = TexMobject("f(x) = e^{x}").scale(0.8).to_corner(UL)
        eq_fd = TexMobject("f'(x) = e^{x}").scale(0.8).next_to(eq.get_part_by_tex("f"), DOWN, aligned_edge = LEFT)
        eq_sd = TexMobject("f''(x) = e^{x}").scale(0.8).next_to(eq_fd.get_part_by_tex("f"), DOWN, aligned_edge = LEFT)
        reminder = TexMobject("e^{0} = 1").scale(0.8).next_to(eq, direction = RIGHT, buff = 1)

        self.play(Write(eq))
        self.wait(15)
        self.play(ReplacementTransform(eq.copy(), eq_fd))
        self.wait(3)
        self.play(ReplacementTransform(eq_fd.copy(), eq_sd))
        self.wait(6)
        self.play(Write(reminder))
        self.wait(7)
        tx = TexMobject("T(x)").next_to(eq_sd.get_part_by_tex("f"), DOWN, aligned_edge = LEFT).set_color(ORANGE)
        eql_sum = TexMobject(r"= \sum_{n=0}^{k}").next_to(tx, RIGHT)
        Full_aprx = TexMobject(r"\frac{f^{\left(n\right)}\left(a\right)}{n!}\cdot\left(x-a\right)^{n}").next_to(eql_sum, RIGHT)
        Full_aprx_2 = TexMobject(r"\frac{1}{n!}\cdot x^{n}").next_to(eql_sum, RIGHT)
        Full_aprx_3 = TexMobject(r"\frac{x^{n}}{n!}").next_to(eql_sum, RIGHT)
        self.play(Write(tx),Write(eql_sum), Write(Full_aprx),)
        self.wait(15)
        self.play(Transform(Full_aprx, Full_aprx_2))
        self.wait(2)
        self.play(Transform(Full_aprx, Full_aprx_3))
        
        for n in range(6):
            self.wait(0.5)
            eql_sum_2 = TexMobject(r"=\sum_{n=0}^{"+ str(n)).next_to(tx, RIGHT)
            if n == 0:
                graph = self.get_graph(functools.partial(taylor_approximation(math.exp,n)), x_min = self.x_min, x_max = self.x_max).set_color(ORANGE)
                self.play(
                    ShowCreation(graph, run_time = 2),
                    Transform(eql_sum, eql_sum_2)
                )

            else:
                new_graph = self.get_graph(functools.partial(taylor_approximation(math.exp, n)), x_min = self.x_min, x_max = self.x_max).set_color(ORANGE)
                self.play(
                    Transform(graph, new_graph, run_time=2),
                    Transform(eql_sum, eql_sum_2)
                )
        
        self.wait(12)
        eql_sum_2 = TexMobject(r"=\sum_{n=0}^{\infty}").next_to(tx, RIGHT)
        eql_exp = TexMobject("= e^{x}").next_to(Full_aprx, RIGHT)
        new_graph = self.get_graph(math.exp, x_min = self.x_min, x_max = self.x_max).set_color(ORANGE)
        self.play(
            Transform(eql_sum, eql_sum_2),
            Write(eql_exp),
            Transform(graph, new_graph, run_time=2),
        )

#wird diese anstatt der allgemeinen Taylorpolynom Berechnung verwendet,
#sind mehr Annäherungsterme möglich, da in TP Berechnung bei zu hoher Termanzahl
#die Berechnung zusammenfällt, da Computer nicht mit den Werten klarkommt, genauer
#Fehler ist mir jedoch unklar
def ln_x_aprx(k,x):
    value = 0
    for n in range(1,k+1):
        value = value + ((-1)**(n+1)*(x-1)**n)/n
    return value

class NoTaylor(GraphScene):
    #LN(x) ANNÄHERUNG BEGINNT BEI n=1
    CONFIG={
        "x_min" : -2,
        "x_max" : 4,
        "x_tick_frequency" : 1,
        "x_axis_label": "",
        "x_axis_width": 13,
        "x_labeled_nums": np.arange(-2,5,2),
        "y_min" : -3,
        "y_max" : 3,
        "y_tick_frequency" : 1, 
        #"y_axis_label": "$f(x)$",
        "y_labeled_nums": np.arange(-2,3,1),
        "graph_origin": 1*DOWN + 3*LEFT
    }

    def setup(self):
        GraphScene.setup(self)

    def construct(self):
        self.setup_axes(animate = True)
        graph = self.get_graph(lambda x: np.log(x), x_min = 0.02).set_color(BLUE)

        ln_x = TexMobject(r"f(x) = ln(x)").set_color(BLUE).to_corner(UR).shift(DOWN+0.5*LEFT)
        derivs = TexMobject(r"f(x) = ln(x)").scale(0.8).to_corner(UL)
        deriv_1 = TexMobject(r"f'(x)=\frac{1}{x}").scale(0.8).next_to(derivs.get_part_by_tex("f"),DOWN, aligned_edge = LEFT, buff = 0)
        deriv_2 = TexMobject(r"f''(x)=-\frac{1}{x^{2}}").scale(0.8).next_to(deriv_1.get_part_by_tex("f"),DOWN, aligned_edge = LEFT, buff = 0)
        deriv_3 = TexMobject(r"f'''(x)=\frac{1\cdot2}{x^{3}}").scale(0.8).next_to(deriv_2.get_part_by_tex("f"),DOWN, aligned_edge = LEFT, buff = 0).shift(0.2*DOWN)
        deriv_4 = TexMobject(r"f''''(x)=-\frac{1\cdot2\cdot3}{x^{4}}").scale(0.8).next_to(deriv_3.get_part_by_tex("f"),DOWN, aligned_edge = LEFT, buff = 0).shift(0.2*DOWN)
        self.play(ShowCreation(graph, run_time = 2))
        self.play(Write(ln_x))
        self.wait(2)
        self.play(Write(derivs))
        self.wait(2)
        self.play(ReplacementTransform(derivs.copy(), deriv_1))
        self.wait(2)
        self.play(ReplacementTransform(deriv_1.copy(), deriv_2))
        self.wait(2)
        self.play(ReplacementTransform(deriv_2.copy(), deriv_3))
        self.wait(2)
        self.play(ReplacementTransform(deriv_3.copy(), deriv_4))
        self.wait(2)

        #COLORING DENOMINATOR
        deriv_1[0][8].set_fill(RED)
        self.wait(2)
        deriv_1[0][8].set_fill(WHITE)
        deriv_2[0][10].set_fill(RED)
        deriv_2[0][11].set_fill(RED)
        self.wait(2)
        deriv_2[0][10].set_fill(WHITE)
        deriv_2[0][11].set_fill(WHITE)
        deriv_3[0][12].set_fill(RED)
        deriv_3[0][13].set_fill(RED)
        self.wait(2)
        deriv_3[0][12].set_fill(WHITE)
        deriv_3[0][13].set_fill(WHITE)
        deriv_4[0][16].set_fill(RED)
        deriv_4[0][17].set_fill(RED)
        self.wait(2)
        deriv_4[0][16].set_fill(WHITE)
        deriv_4[0][17].set_fill(WHITE)
        self.wait(2)

        #COLORING NUMERATOR
        deriv_1[0][6].set_fill(RED)
        self.wait(2)
        deriv_1[0][6].set_fill(WHITE)
        deriv_2[0][8].set_fill(RED)
        self.wait(2)
        deriv_2[0][8].set_fill(WHITE)
        deriv_3[0][8].set_fill(RED)
        deriv_3[0][10].set_fill(RED)
        self.wait(2)
        deriv_3[0][8].set_fill(WHITE)
        deriv_3[0][10].set_fill(WHITE)
        deriv_4[0][10].set_fill(RED)
        deriv_4[0][12].set_fill(RED)
        deriv_4[0][14].set_fill(RED)
        self.wait(2)
        deriv_4[0][10].set_fill(WHITE)
        deriv_4[0][12].set_fill(WHITE)
        deriv_4[0][14].set_fill(WHITE)
        self.wait(2)

        p1 = TexMobject("1").next_to(derivs, RIGHT, buff = 0.1).shift(0.23*UP)
        p2 = TexMobject("2").next_to(derivs, RIGHT, buff = 1.5)
        arrow = Arrow(p1,p2 )
        self.play(ShowCreation(arrow))

        nth = TexMobject(r"f^{(n)}(x)=(-1)^{n+1}\cdot\frac{(n-1)!}{x^{n}}").scale(0.8).next_to(derivs, RIGHT, buff = 1.7)
        self.play(ReplacementTransform(derivs.copy(), nth))
        self.wait(2)

        #Definitionslücke x=0
        def_line = DashedLine(*[
            self.coords_to_point(0,y)
            for y in (self.y_min, self.y_max)
        ]).set_color(YELLOW)
        self.play(GrowFromCenter(def_line))
        self.wait(2)

        nth_1 = TexMobject(r"f^{(n)}(1)=(-1)^{n+1}\cdot\frac{(n-1)!}{1^{n}}").scale(0.8).next_to(derivs, RIGHT, buff = 1.7)
        self.play(Transform(nth, nth_1))
        self.play(FadeOut(def_line))
        nth_2 = TexMobject(r"f^{(n)}(1)=(-1)^{n+1}\cdot",r"\frac{(n-1)!}{1^{n}}").scale(0.8).next_to(derivs, RIGHT, buff = 1.7)
        self.add(nth_2)
        self.remove(nth)
        self.wait(2)
        nth_1 = TexMobject(r"(n-1)!").scale(0.8).next_to(derivs, RIGHT, buff = 1.7).shift(3.5*RIGHT+0.05*DOWN)
        self.play(Transform(nth_2[-1], nth_1))
        self.wait(2)
        taylor = TexMobject(r"ln(x)", r"\approx", r"\sum_{n=1}^{k}",r"\frac{f^{(n)}(1)}{n!}",r"\cdot\left(x-1\right)^{n}").scale(0.8).shift(UP)
        self.play(Write(taylor))
        ln_apx = TexMobject(r"\frac{\left(-1\right)^{n+1}\cdot\left(n-1\right)!}{n!}").scale(0.8).shift(1.06*UP+1.06*RIGHT)
        self.play(
            Transform(taylor[3], ln_apx),
            taylor[-1].shift,1.75*RIGHT
        )
        self.wait(2)
        ln_apx_1 = TexMobject(r"\frac{\left(-1\right)^{n+1}}{n}").scale(0.8).shift(1.07*UP+0.3*RIGHT)
        self.play(
            Transform(taylor[3], ln_apx_1),
            taylor[-1].shift,1.6*LEFT
        )
        self.wait(2)
        self.play(
            FadeOut(ln_x),
            taylor.shift, 3*RIGHT+1*UP,
        )

        taylor[0].set_fill(BLUE),
        taylor[2].set_fill(GREEN),
        taylor[3].set_fill(GREEN),
        taylor[4].set_fill(GREEN),
        self.wait(2)

        dot = Dot()
        dot.move_to(self.coords_to_point(1,0))
        self.play(
            FadeIn(dot),
            dot.set_fill, PURPLE, 1,
        )
        self.foreground_mobjects.append(dot)
        
        #Because of LaTeX Error: converting to DVI it's not possible to put a variable into the Tex Formula
        # => this ugly array
        sigmas = [TexMobject(r"\sum_{n=1}^{1}"), TexMobject(r"\sum_{n=1}^{2}"),TexMobject(r"\sum_{n=1}^{3}"), TexMobject(r"\sum_{n=1}^{4}"), TexMobject(r"\sum_{n=1}^{5}"),
                TexMobject(r"\sum_{n=1}^{6}"), TexMobject(r"\sum_{n=1}^{7}"), TexMobject(r"\sum_{n=1}^{8}"), TexMobject(r"\sum_{n=1}^{9}"), TexMobject(r"\sum_{n=1}^{10}"),
                TexMobject(r"\sum_{n=1}^{11}"), TexMobject(r"\sum_{n=1}^{12}"), TexMobject(r"\sum_{n=1}^{13}"), TexMobject(r"\sum_{n=1}^{14}"), TexMobject(r"\sum_{n=1}^{15}"),
                TexMobject(r"\sum_{n=1}^{16}"), TexMobject(r"\sum_{n=1}^{17}"), TexMobject(r"\sum_{n=1}^{18}"), TexMobject(r"\sum_{n=1}^{19}"), TexMobject(r"\sum_{n=1}^{20}"),
                TexMobject(r"\sum_{n=1}^{10}"), TexMobject(r"\sum_{n=1}^{15}"), TexMobject(r"\sum_{n=1}^{20}"), TexMobject(r"\sum_{n=1}^{25}"), TexMobject(r"\sum_{n=1}^{30}"), ]
        
        for n in range (5):
            sigma = sigmas[n]
            sigma.scale(0.8).shift(2*UP+2.1*RIGHT).set_color(GREEN)
            if n == 0:
                graph = self.get_graph(functools.partial(ln_x_aprx, n+1)).set_color(GREEN)
                self.play(
                    ShowCreation(graph, run_time = 2),
                    Transform(taylor[2], sigma),
                    #Animate(dot)#sonst graph über dem Punkt
                )
            else:
                new_graph =self.get_graph(functools.partial(ln_x_aprx, n+1)).set_color(GREEN)
                self.play(
                    Transform(graph, new_graph, run_time = 2),
                    Transform(taylor[2], sigma),
                    #Animate(dot)#sonst graph über dem Punkt
                )
            self.wait(2/math.sqrt(n+1))

        new_graph =self.get_graph(functools.partial(ln_x_aprx, 5), x_min = -0.3, x_max = 3).set_color(GREEN)
        self.add(new_graph)
        self.remove(graph)

        for n in range(1,4):
            sigma = sigmas[n+19]
            sigma.scale(0.8).shift(2*UP+2.1*RIGHT).set_color(GREEN)
            new_graph_2 =self.get_graph(functools.partial(ln_x_aprx, 5*(n+1)), x_min = -0.3, x_max = 3).set_color(GREEN)
            self.play(
                Transform(new_graph, new_graph_2, run_time = 2),
                Transform(taylor[2], sigma),
                #Animate(dot)#sonst graph über dem Punkt
            )
            self.wait(2/math.sqrt(5*n+1))
        
        self.wait(2)
        #Konvergenzradius
        lines = [
            DashedLine(*[
                self.coords_to_point(x,y)
                for y in (-3, 3)
            ])
            for x in (0,1,2)
        ]
        outer_lines = VGroup(*lines[::2]).set_color(YELLOW)
        #outer_lines.add_background_rectangle()
        center_line = VGroup(lines[1]).set_color(YELLOW)
        self.play(
            GrowFromCenter(center_line),
            #Animate(dot)#sonst graph über dem Punkt
        )
        self.wait(2)
        self.play(Transform(center_line, outer_lines, run_time = 2))
        self.wait(2)
        line = Line(*[
            self.coords_to_point(x,0)
            for x in (1,2)
        ])
        line.set_color(PURPLE)
        brace = Brace(line, UP)
        kvgrd = brace.get_text("Konvergenzradius")
        kvgrd.add_background_rectangle()

        self.play(
            GrowFromCenter(brace),
            ShowCreation(line)
        )
        self.wait(2)
        self.play(Write(kvgrd))
        self.wait(2)
        self.play(FadeOut(VGroup(*self.mobjects)), FadeOut(dot))
        self.wait(2)

def fourier(a, x):
    value = 0
    for n in range(1,a+1):
        value += -2/(math.pi*n)*math.sin(n*math.pi*x)
    return value 

class FourierReihe(GraphScene):
    CONFIG = {
        "x_min": -7,
        "x_max": 7,
        "y_min": -3,
        "y_max": 4,
        "x_axis_width": 12,
        "graph_origin": ORIGIN
    }

    

    def construct(self):
        self.setup_axes(animate = True)
        self.wait(2)
        graph = self.get_graph(functools.partial(fourier, 0)).set_color(BLUE)
        self.play(ShowCreation(graph))
        for n in range(1,8):
            new_graph = self.get_graph(functools.partial(fourier, n)).set_color(BLUE)
            if n ==1:
                self.play(Transform(graph, new_graph, run_time = 1))
            else:
                self.play(Transform(graph, new_graph, run_time = 0.3))
            self.wait(0.3)
        self.play(FadeOut(VGroup(*self.mobjects)))

class Sources(Scene):


    def construct(self):
        danke = TextMobject("Danke für eure Aufmerksamkeit").scale(1.5)
        self.play(Write(danke))
        self.wait(5)
        self.play(FadeOutAndShift(danke, DOWN))
        self.wait(2)
        sources = TextMobject("Quellen:").to_corner(UL)
        source_1 = TextMobject("https://de.wikipedia.org/wiki/Taylorreihe").scale(0.5).next_to(sources, DOWN).to_edge(LEFT)
        source_2 = TextMobject("https://de.wikipedia.org/wiki/Newtonverfahren").scale(0.5).next_to(source_1, DOWN).to_edge(LEFT)
        source_3 = TextMobject("https://www.matheretter.de/wiki/restgliedabschatzung").scale(0.5).next_to(source_2, DOWN).to_edge(LEFT)
        source_4 = TextMobject("https://www.youtube.com/watch?v=3d6DsjIBzJ4").scale(0.5).next_to(source_3, DOWN).to_edge(LEFT)
        source_5 = TextMobject("https://www.youtube.com/watch?v=ELPvMyhNrz8").scale(0.5).next_to(source_4, DOWN).to_edge(LEFT)
        source_6 = TextMobject("Musik: https://vincerubinetti.bandcamp.com/album/the-music-of-3blue1brown").scale(0.5).next_to(source_5, DOWN).to_edge(LEFT)
        self.play(FadeIn(sources))
        self.play(AnimationGroup(
            FadeIn(source_1, run_time = 1.5),
            FadeIn(source_2, run_time = 1.5),
            FadeIn(source_3, run_time = 1.5),
            FadeIn(source_4, run_time = 1.5),
            FadeIn(source_5, run_time = 1.5),
            FadeIn(source_6, run_time = 1.5),
            lag_ratio = 0.3,
        ))

class Beispiel(GraphScene):
    CONFIG = {
        "x_min" : -5,
        "x_max" : 5,
        "x_tick_frequency" : 1,
        "x_axis_label": "$x$",
        "x_axis_width": 13,
        "y_min" : 0,
        "y_max" : 3,
        "y_tick_frequency" : 1,
        "y_axis_label": "$x$", 
        "graph_origin": 3*DOWN,

    } 

    def construct(self):
        self.setup_axes(animate = True)
        graph = self.get_graph(lambda x: math.exp(-(x-1)**2)).set_color(BLUE)
        formula = TexMobject(r"f\left(x\right) = e^{-\left(x-1\right)^{2}}").set_color(BLUE).to_corner(UR).shift(3.5*DOWN, 1.5*LEFT)
        self.wait()
        self.play(
            AnimationGroup(
                ShowCreation(graph),
                Write(formula),
                lag_ratio = 0.3
            )
        )
        self.wait(2) 
    
class Introduction(GraphScene):
    CONFIG = {
            "x_min" : -1,
            "x_max" : 3,
            "x_tick_frequency" : 1,
            "x_axis_label": "$x$",
            "x_axis_width": 9,
            "y_min" : -3,
            "y_max" : 8,
            "y_tick_frequency" : 1,
            "y_axis_label": "$y$", 
            "graph_origin": 2*DOWN + 3*LEFT,
    } 

    def construct(self):
        def func(x):
            return (4+2*x-0.6*x**2+9*x**3-7*x**4)
        self.wait(2)
        self.setup_axes(animate = True)
        graph = self.get_graph(func).set_color(BLUE)
        formula = TexMobject(r"f\left(x\right) = ",r"4", r"+2x", r"-0.6x^{2}", r"+9x^{3}", r"-7x^{4}").scale(0.8).set_color(BLUE).to_corner(UR).shift(2.8*DOWN)
        g_x = [TexMobject(r"g(x) = 4").scale(0.8).next_to(formula.get_part_by_tex(r"f"), DOWN, aligned_edge = LEFT).set_color(ORANGE),
             TexMobject(r"+2x").scale(0.8).next_to(formula.get_part_by_tex("+2x"), DOWN, aligned_edge = LEFT).set_color(ORANGE).shift(0.1*DOWN), 
             TexMobject(r"-0.6x^{2}").scale(0.8).next_to(formula.get_part_by_tex("-0.6x^{2}"), DOWN, aligned_edge = LEFT).set_color(ORANGE).shift(0.05*DOWN), 
             TexMobject(r"+9x^{3}").scale(0.8).next_to(formula.get_part_by_tex("+9x^{3}"), DOWN, aligned_edge = LEFT).set_color(ORANGE).shift(0*DOWN), 
             TexMobject(r"-7x^{4}").scale(0.8).next_to(formula.get_part_by_tex("-7x^{4}"), DOWN, aligned_edge = LEFT).set_color(ORANGE)
            ]
        self.wait(0.5)
        self.play(
            AnimationGroup(
                ShowCreation(graph, run_time = 2.5),
                Write(formula),
                lag_ratio = 0.3
            )
        )
        self.foreground_mobjects.append(formula)
        self.wait(2)
        dot = Dot()
        dot.move_to(self.coords_to_point(0,0)).set_color(RED)
        self.play(FadeIn(dot))
        self.wait()
        self.play(dot.move_to, self.coords_to_point(0, 4))
        self.foreground_mobjects.append(dot)
        line = Line(*[
                self.coords_to_point(x,4)
                for x in (self.x_min,self.x_max)
                ]).set_color(ORANGE)
        self.play(
            AnimationGroup(
                GrowFromPoint(line,self.coords_to_point(0,4)),
                Write(g_x[0]),
                lag_ratio = 0.5
            )
        )
        self.wait()
        for n in range(1,5):
            graph_2 = self.get_graph(taylor_approximation(func, n)).set_color(ORANGE)
            self.play(AnimationGroup(
                Transform(line, graph_2, run_time = 2),
                Write(g_x[n]),
                lag_ratio = 0.5
                )
            )
            self.wait()
        self.wait(2)
        