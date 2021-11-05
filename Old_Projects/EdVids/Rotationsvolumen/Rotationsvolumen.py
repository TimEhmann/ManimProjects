from manimlib.imports import *
import numpy as np
import math
import functools

class RV(ThreeDScene):
    def construct(self):
        axis_config = {
            "x_min": -2,
            "x_max": 7,
            "y_min": -5,
            "y_max": 5,
            "z_min": -5,
            "z_max": 5,
        }
        
        axes = ThreeDAxes(**axis_config)
        
        func = FunctionGraph(lambda x: 1/x, x_min = 0.01)
        func2 = FunctionGraph(lambda x: 1/x, x_min=1)
        

        surface = ParametricSurface(
            lambda u,v: np.array([
                u,
                (1/u)*np.cos(v),
                (1/u)*np.sin(v)
            ]),
            u_min = 1,
            u_max = 7,
            v_min = 0,
            v_max = 0.001,
            checkerboard_colors=[eval(key) for key in COLOR_MAP.keys()],
            fill_color = YELLOW,
            stroke_color = WHITE,
        )
        circle = ParametricSurface(
            lambda u,v: np.array([
                1,
                (1/u)*np.cos(v),
                (1/u)*np.sin(v)
            ]),
            u_min = 1,
            u_max = 120,
            v_min = 0,
            v_max = 2*np.pi,
            checkerboard_colors = [RED],
            fill_color = RED,
            stroke_color = RED
        )
        surface_avg = ParametricSurface(
            self.surface_avg,
            u_min = 1,
            u_max = 7,
            v_min = 0,
            v_max = 2*np.pi,
            checkerboard_colors=[eval(key) for key in COLOR_MAP.keys()],
            fill_color = YELLOW,
            stroke_color = WHITE,
        )
        circle_avg = ParametricSurface(
            lambda u,v: np.array([
                1,
                0.45*u*np.cos(v),
                0.45*u*np.sin(v)
            ]),
            u_min = 1/200,
            u_max = 1,
            v_min = 0,
            v_max = 2*np.pi,
            checkerboard_colors = [RED],
            fill_color = RED,
            stroke_color = RED
        )
        circle2 = ParametricSurface(
            self.circle2,
            u_min = 0,
            u_max = 2*np.pi,
            v_min = 0,
            v_max = 1/5,
            fill_color = RED,
            stroke_color = RED,
            checkerboard_colors = [RED],
        )

        self.play(Write(func), Write(axes))
        self.wait()

        self.play(Transform(func, func2), Write(surface))
        self.wait()

        
        self.move_camera(0.8 * np.pi / 2, -0.45 * np.pi)
        #self.begin_ambient_camera_rotation(rate= 0.04)
        #Rotationskörper
        self.remove(func)
        self.play(
            UpdateFromAlphaFunc(surface, self.update_f),
            rate_func = linear,
            run_time = 2
        )

        #Seitenansciht und Querschnitt
        self.wait(5)
        self.move_camera(np.pi / 2 , -np.pi)
        self.wait(2)
        self.play(ShowCreation(circle))
        self.wait()
        self.move_camera(0.8*np.pi/2, -np.pi/2 - 0.2)
        self.wait()

        #Transparenz und unterschied der Querschnitte

        surface.set_fill(opacity=0.5)
        surface.set_stroke(opacity=0.5)
        self.play(Write(circle2))
        self.wait()
        self.play(Uncreate(surface.save_state()))
        self.wait()
        self.play(ShowCreation(surface.restore()))
        self.wait()
        surface.set_fill(opacity=1)
        surface.set_stroke(opacity=1)
        self.remove(circle2)
        self.wait()

        #Transformation in den Durchschnittszylinder
        self.play(ReplacementTransform(surface.save_state(), surface_avg), ReplacementTransform(circle.save_state(), circle_avg))
        self.wait()
        surface_avg.set_fill(opacity=0.5)
        surface_avg.set_stroke(opacity=0.5)
        circle_copy = circle
        self.add(circle_copy)
        self.play(circle_copy.shift, 6*RIGHT, run_time = 2)
        self.play(FadeOut(circle))
        self.wait()
        height = TexMobject(r"h = b-a").shift(3*UP+5*RIGHT).rotate(PI/2, axis = RIGHT)
        height[0][0].set_color(ORANGE)
        self.play(Write(height))
        self.wait()
        
        #Rücktransformation in den anfänglichen Rotationskörper
        self.play(ReplacementTransform(surface_avg, surface.restore()), ReplacementTransform(circle_avg, circle.restore()))
        self.wait()

    def update_f(self, c, dt):
        a =interpolate(0.1, 2*PI, dt)
        s = ParametricSurface(
            self.surface,
            u_min = 1,
            u_max = 7,
            v_min = 0,
            v_max = a,
            checkerboard_colors = [eval(key) for key in COLOR_MAP.keys()],
            color = YELLOW,
            fill_color = YELLOW
        )
        c.become(s)
    
    @staticmethod
    def circle2(u, v):
        return np.array([
            5,
            v*np.cos(u),
            v*np.sin(u)
        ])
    
    @staticmethod
    def surface(u, v):
        return np.array([
            u,
            (1/u)*np.cos(v),
            (1/u)*np.sin(v)
        ])

    @staticmethod
    def surface_avg(u,v):
        return np.array([
            u,
            0.45*np.cos(v),
            0.45*np.sin(v)
        ])
        
class Formel(Scene):
    def construct(self):
        fI = TexMobject(r"A(r) = \pi \cdot r^{2}").scale(0.8).to_edge(UP + LEFT)
        fI_2 = TexMobject(r"A(x) = \pi \cdot f \left( x \right) ^{2}").scale(0.8).next_to(fI, direction = DOWN, aligned_edge = LEFT, buff = 0.6)
        v_1 = TexMobject(r"V = {\bar {G}}*h").scale(0.8).next_to(fI_2, direction = DOWN, aligned_edge = LEFT, buff = 0.6)
        
        avge = TexMobject(r"{\bar {G}} = {\bar {A}} = \frac{1}{b-a}\int_{a}^{b}A\left(x\right)dx").scale(0.8).next_to(v_1, direction = DOWN, aligned_edge = LEFT, buff = 0.6)
        avge.add_background_rectangle()
        avge[1][0].set_color(RED)
        avge[1][1].set_color(RED)
        avge[1][8].set_color(GREEN)
        avge[1][12].set_color(GREEN)
        avge[1][10].set_color(BLUE)
        avge[1][13].set_color(BLUE)
        
        v_2 = TexMobject(r"V = \frac{1}{b-a}\int_{a}^{b}A\left(x\right)dx \cdot h").scale(0.8).next_to(avge, direction = DOWN, aligned_edge = LEFT, buff = 0.6)
        v_2[0][4].set_color(GREEN)
        v_2[0][8].set_color(GREEN)
        v_2[0][6].set_color(BLUE)
        v_2[0][9].set_color(BLUE)
        v_2[0][-1].set_color(ORANGE)
        v_2_transform = TexMobject(r"(b-a)").scale(0.8).next_to(v_2, aligned_edge=RIGHT).shift(0.08*RIGHT + 0.05*DOWN)
        v_2_transform[0][1].set_color(BLUE)
        v_2_transform[0][3].set_color(GREEN)

        v_3 = TexMobject(r"V = \int_{a}^{b}\pi\cdot f\left(x\right)^{2}dx").scale(0.8).next_to(v_2, direction = DOWN, aligned_edge = LEFT, buff = 0.6)
        v_3[0][3].set_color(GREEN)
        v_3[0][4].set_color(BLUE)

        self.wait()
        self.play(Write(fI))
        self.wait()
        self.play(Write(fI_2))
        self.wait()
        self.play(Write(v_1))
        self.wait()
        self.play(Write(avge),FadeToColor(v_1[0][2],RED),FadeToColor(v_1[0][3],RED), FadeToColor(v_1[0][5], ORANGE))
        self.wait()
        self.play(Write(v_2))
        self.wait()
        self.play(Transform(v_2[0][-1], v_2_transform))
        self.wait()
        self.play(Write(v_3))
        self.wait()
        coeff = VGroup(v_3[0][5],v_3[0][6])
        integral = VGroup(v_3[0][2],v_3[0][3],v_3[0][4])
        self.play(coeff.shift,0.5*LEFT, integral.shift, 0.6*RIGHT)
        self.wait()
        rect = Rectangle(height=1.2, width=4,color = RED).shift(4.85*LEFT+3.3*DOWN)
        self.play(FadeIn(rect))
        self.wait()
        self.play(VGroup(*self.mobjects).shift, 10*LEFT)
        self.wait()

class Function(Scene):
    def construct(self):
        functerm = TexMobject(r"f(x) = \frac{1}{x}").scale(0.8).to_corner(UP + RIGHT).shift(2*LEFT)
        interval = TexMobject(r"x \in [1,7]").scale(0.8).next_to(functerm, aligned_edge=RIGHT, buff = 1.2)
        self.play(Write(functerm))
        self.wait()
        self.play(Write(interval))
        self.wait()

class Methode2(ThreeDScene):
    def construct(self):
        axis_config = {
            "x_min": -2,
            "x_max": 7,
            "y_min": -5,
            "y_max": 5,
            "z_min": -5,
            "z_max": 5,
        }
        
        axes = ThreeDAxes(**axis_config)
        
        func = FunctionGraph(lambda x: 1/x, x_min = 0.01)
        func2 = FunctionGraph(lambda x: 1/x, x_min=1)
        

        surface = ParametricSurface(
            lambda u,v: np.array([
                u,
                (1/u)*np.cos(v),
                (1/u)*np.sin(v)
            ]),
            u_min = 1,
            u_max = 7,
            v_min = 0,
            v_max = 0.001,
            checkerboard_colors=[MAROON],
            fill_color = YELLOW,
            stroke_color = WHITE,
        )
        disk = ParametricSurface(
            lambda u,v: np.array([
                -2,
                u*np.cos(v),
                u*np.sin(v)
            ]),
            u_min = 0,
            u_max = 0.5,
            v_min = 0,
            v_max = 2*np.pi,
            checkerboard_colors = [RED, ORANGE],
            fill_color = WHITE,
            stroke_color = WHITE
        )
        disk2 = ParametricSurface(
            lambda u,v: np.array([
                0,
                u*np.cos(v),
                u*np.sin(v)
            ]),
            u_min = 0,
            u_max = 2.5,
            v_min = 0,
            v_max = 2*np.pi,
            checkerboard_colors = [RED, ORANGE],
            fill_color = WHITE,
            stroke_color = WHITE
        )

        self.play(Write(func), Write(axes))
        self.wait()

        self.play(Transform(func, func2), Write(surface))
        self.wait()

        
        self.move_camera(0.8 * np.pi / 2, -0.45 * np.pi)
        #Rotationskörper
        self.remove(func)
        self.play(
            UpdateFromAlphaFunc(surface, self.update_f),
            rate_func = linear,
            run_time = 2
        )

        #zoom an den Körper
        self.play(Uncreate(axes), surface.center)
        self.wait()
        surface.set_stroke(opacity = 0.5)
        surface.set_fill(opacity = 0.5)
        self.wait()

        self.play(Write(disk))
        self.wait()
        self.play(Uncreate(surface))

        self.move_camera(phi = np.pi/2, theta = 0, distance=3)
        line = ParametricFunction(
            lambda u: np.array([
                1.8,
                0,
                u
            ]),
            u_min = 0,
            u_max = 1,
            color = YELLOW,
        )
        self.play(Transform(disk, disk2))
        self.wait()
        self.play(Write(line))
        self.wait()

    def update_f(self, c, dt):
        a =interpolate(0.1, 2*PI, dt)
        s = ParametricSurface(
            lambda u,v: np.array([
                u,
                (1/u)*np.cos(v),
                (1/u)*np.sin(v)
            ]),
            u_min = 1,
            u_max = 7,
            v_min = 0,
            v_max = a,
            checkerboard_colors = [eval(key) for key in COLOR_MAP.keys()],
            color = YELLOW,
            fill_color = YELLOW
        )
        c.become(s)

class Methode2Text(Scene):
    def construct(self):
        radius = TexMobject(r"r = f(x) = \frac{1}{x}").to_edge(UP)
        radius[0][0].set_color(YELLOW)

        v1 = TexMobject(r"V = G \cdot h")
        v1.scale(0.8).to_corner(UL)
        v1[0][2].set_color(GREEN)
        v1[0][4].set_color(BLUE)

        v2 = TexMobject(r"V = \pi \cdot r^{2} \cdot dx")
        v2.scale(0.8).next_to(v1, direction = DOWN, aligned_edge=LEFT, buff=0.6)
        v2[0][2].set_color(GREEN)
        v2[0][4].set_color(GREEN)
        v2[0][5].set_color(GREEN)
        v2[0][7].set_color(BLUE)
        v2[0][8].set_color(BLUE)

        v3 = TexMobject(r"V = \int_{a}^{b} \pi\cdot f\left(x\right)^{2}dx")
        v3.scale(0.8).next_to(v2, direction=DOWN, aligned_edge= LEFT, buff = 0.6)
        v3[0][5].set_color(GREEN)
        v3[0][7].set_color(GREEN)
        v3[0][8].set_color(GREEN)
        v3[0][9].set_color(GREEN)
        v3[0][10].set_color(GREEN)
        v3[0][11].set_color(GREEN)
        v3[0][12].set_color(BLUE)
        v3[0][13].set_color(BLUE)

        self.play(Write(radius))
        self.wait()
        self.play(Write(v1))
        self.wait()
        self.play(Write(v2))
        self.wait()
        self.play(Write(v3))
        self.wait()
        coeff = VGroup(v3[0][5],v3[0][6])
        integral = VGroup(v3[0][2],v3[0][3],v3[0][4])
        self.play(coeff.shift,0.5*LEFT, integral.shift, 0.6*RIGHT)
        self.wait()
        rect = Rectangle(height=1.2, width=4,color = RED).shift(4.85*LEFT+1.15*UP)
        self.play(FadeIn(rect))
        self.wait()

class Beispiel(ThreeDScene):
    def construct(self):
        axis_config = {
            "x_min": 0,
            "x_max": 60,
            "y_min": -7,
            "y_max": 7,
            "z_min": -7,
            "z_max": 7,
        }
        
        axes = ThreeDAxes(**axis_config)
        
        func = FunctionGraph(lambda x: math.sqrt(6*x), x_min = 0, x_max = 6)
        func2 = FunctionGraph(lambda x: math.sqrt(4*x-8), x_min=2, x_max = 6)

        self.play(Write(axes), Write(func), Write(func2))

        self.move_camera(0.8 * np.pi / 2, -0.75 * np.pi, distance=800)
        surface1 = ParametricSurface(
            lambda u,v: np.array([
                u,
                math.sqrt(6*u)*np.cos(v),
                math.sqrt(6*u)*np.sin(v),
            ]),
            u_min = 0.01,
            u_max = 6,
            v_min = 0,
            v_max = 2*np.pi,
            color = WHITE,
            fill_color = WHITE,
            checkerboard_colors = [RED],
        )
        surface2 = ParametricSurface(
            lambda u,v: np.array([
                u,
                math.sqrt(4*u-8)*np.cos(v),
                math.sqrt(4*u-8)*np.sin(v),
            ]),
            u_min = 2.01,
            u_max = 6,
            v_min = 0,
            v_max = 2*np.pi,
            color = WHITE,
            fill_color = WHITE,
            checkerboard_colors = [GREEN],
        )
        surface3 = ParametricSurface(
            lambda u,v: np.array([
                6,
                u*np.cos(v),
                u*np.sin(v)
            ]),
            u_min = 4,
            u_max = 6,
            v_min = 0,
            v_max = 2*np.pi,
            color = WHITE,
            fill_color = WHITE,
            checkerboard_colors = [BLUE]
        )
        surface1.set_fill(opacity = 0.5)
        surface1.set_stroke(opacity = 0.5)
        self.begin_ambient_camera_rotation(rate = 0.035)
        #Rotationkörper
        self.remove(func2)
        self.play(Write(surface2, run_time = 2))
        self.wait()
        self.remove(func)
        self.play(Write(surface1, run_time = 2))
        self.wait()
        self.play(Write(surface3, run_time = 2))
        self.wait(8)
        self.stop_ambient_camera_rotation()

class BeispielRechnung(Scene):
    def construct(self):
        f_1 = TexMobject(r" p\left(x\right)=\sqrt{6x} ").scale(0.5).to_corner(UL)
        f_1[0][0].set_color(RED)
        f_1[0][1].set_color(RED)
        f_1[0][2].set_color(RED)
        f_1[0][3].set_color(RED)
        f_1_int = TexMobject(r" x \in [0,6] ").scale(0.5).next_to(f_1, aligned_edge= RIGHT, buff = 1.4)
        f_2 = TexMobject(r" q\left(x\right)=\sqrt{4x-8} ").scale(0.5).next_to(f_1, direction = DOWN, aligned_edge=LEFT, buff = 0.4)
        f_2[0][0].set_color(GREEN)
        f_2[0][1].set_color(GREEN)
        f_2[0][2].set_color(GREEN)
        f_2[0][3].set_color(GREEN)
        f_2_int = TexMobject(r" x \in [2,6] ").scale(0.5).next_to(f_2, aligned_edge= RIGHT, buff = 1)

        self.play(Write(f_1))
        self.play(Write(f_1_int))
        self.play(Write(f_2))
        self.play(Write(f_2_int))
        self.wait()

        v_0 = TexMobject(r"V\ =\ V_{p} - V_{q}").scale(0.5).next_to(f_2, direction = DOWN, aligned_edge=LEFT, buff = 0.4)
        v_0[0][2].set_color(RED)
        v_0[0][3].set_color(RED)
        v_0[0][5].set_color(GREEN)
        v_0[0][6].set_color(GREEN)
        v_1 = TexMobject(r"V\ =\ \pi\cdot\int_{0}^{6}p\left(x\right)^{2}dx - \pi\cdot\int_{2}^{6}q\left(x\right)^{2}dx").scale(0.5).next_to(v_0, direction = DOWN, aligned_edge=LEFT, buff = 0.4)
        for i in range(12):
            v_1[0][2+i].set_color(RED)
            v_1[0][15+i].set_color(GREEN)
        v_2 = TexMobject(r"V\ =\ \pi\cdot\int_{0}^{6}\left(\sqrt{6x}\right)^{2}dx-\pi\cdot\int_{2}^{6}\left(\sqrt{4x-8}\right)^{2}dx").scale(0.5).next_to(v_1, direction = DOWN, aligned_edge=LEFT, buff = 0.4)
        v_3 = TexMobject(r"V\ =\ \pi\cdot\int_{0}^{6}6x\ dx-\pi\cdot\int_{2}^{6}\left(4x-8\right)dx").scale(0.5).next_to(v_2, direction = DOWN, aligned_edge=LEFT, buff = 0.4)
        v_4 = TexMobject(r"V\ =\ \pi\cdot\left[3x^{2}\right]_0^6 - \pi\cdot\left[2x^{2}-8x\right]_2^6").scale(0.5).next_to(v_3, direction = DOWN, aligned_edge=LEFT, buff = 0.4)
        v_5 = TexMobject(r"V\ =\ \pi\cdot3\cdot6^{2}-\pi\cdot\left(\left(2\cdot6^{2}-8\cdot6\right)-\left(2\cdot2^{2}-8\cdot2\right)\right)").scale(0.5).next_to(v_4, direction = DOWN, aligned_edge=LEFT, buff = 0.4)
        v_6 = TexMobject(r"V\ =\ \pi\cdot108-\pi\cdot\left(24-\left(-8\right)\right)").scale(0.5).next_to(v_5, direction = DOWN, aligned_edge=LEFT, buff = 0.4)
        v_7 = TexMobject(r"V\ =\ 76\cdot\pi").scale(0.5).next_to(v_6, direction = DOWN, aligned_edge=LEFT, buff = 0.4)

        self.play(Write(v_0))
        self.wait()
        self.play(Write(v_1))
        self.wait()
        self.play(Write(v_2))
        self.wait()
        self.play(Write(v_3))
        self.wait()
        self.play(Write(v_4))
        self.wait()
        self.play(Write(v_5))
        self.wait()
        self.play(Write(v_6))
        self.wait()
        self.play(Write(v_7))
        self.wait()
        self.play(FadeOutAndShift(v_0, direction = LEFT),FadeOutAndShift(v_1, direction = LEFT),FadeOutAndShift(v_2, direction = LEFT),FadeOutAndShift(v_3, direction = LEFT),FadeOutAndShift(v_4, direction = LEFT),FadeOutAndShift(v_5, direction = LEFT),FadeOutAndShift(v_6, direction = LEFT),FadeOutAndShift(v_7, direction = LEFT))

        m_0 = TexMobject(r"\rho = 2700\frac{kg}{m^{3}}").scale(0.5).next_to(f_2, direction = DOWN, aligned_edge=LEFT, buff = 0.4)
        m_0_1 = TexMobject(r"V = 76\cdot\pi \cdot dm^{3}").scale(0.5).next_to(m_0, aligned_edge= RIGHT, buff = 1)
        m_1 = TexMobject(r"m = \rho \cdot V").scale(0.5).next_to(m_0, direction = DOWN, aligned_edge=LEFT, buff = 0.4)
        m_2 = TexMobject(r"m = 2700\frac{kg}{m^{3}} \cdot 76\cdot\pi \cdot dm^{3}").scale(0.5).next_to(m_1, direction = DOWN, aligned_edge=LEFT, buff = 0.4)
        m_3 = TexMobject(r"m = 2700\frac{kg}{m^{3}} \cdot 76\cdot\pi\frac{m^{3}}{10^{3}}").scale(0.5).next_to(m_2, direction = DOWN, aligned_edge=LEFT, buff = 0.4)
        m_4 = TexMobject(r"m \approx 645kg").scale(0.5).next_to(m_3, direction = DOWN, aligned_edge=LEFT, buff = 0.4)

        self.play(Write(m_0))
        self.wait()
        self.play(Write(m_1))
        self.wait()
        self.play(Write(m_2))
        self.wait()
        self.play(Write(m_3))
        self.wait()
        self.play(Write(m_4))
        self.wait()

class Intro(Scene):
    def construct(self):
        title = TextMobject("Rotationsvolumen einer Funktion").shift(UP*1)
        subtitle = TextMobject("2 Methoden zur Herleitung").shift(DOWN*0.5)

        self.play(Write(title))
        self.wait()
        self.play(Write(subtitle))
        self.wait()
        self.play(FadeOutAndShiftDown(title), FadeOutAndShiftDown(subtitle))
        self.wait()
        m1 = TextMobject("Methode 1: Durschnittliche Querschnittfläche")
        self.play(Write(m1))
        self.wait()
        self.play(FadeOutAndShiftDown(m1))
        self.wait()
        m2 = TextMobject("Methode 2: Infinitesimalrechnung")
        self.play(Write(m2))
        self.wait()
        self.play(FadeOutAndShiftDown(m2))
        self.wait()

class methode2_rework2(ThreeDScene):
    def construct(self):
        axis_config = {
            "x_min": -2,
            "x_max": 7,
            "y_min": -5,
            "y_max": 5,
            "z_min": -5,
            "z_max": 5,
        }
        
        axes = ThreeDAxes(**axis_config)
        
        func = FunctionGraph(lambda x: 1/x, x_min = 0.01)
        func2 = FunctionGraph(lambda x: 1/x, x_min=1)
        

        surface = ParametricSurface(
            lambda u,v: np.array([
                u,
                (1/u)*np.cos(v),
                (1/u)*np.sin(v)
            ]),
            u_min = 1,
            u_max = 7,
            v_min = 0,
            v_max = 0.001,
            checkerboard_colors=[MAROON],
            fill_color = YELLOW,
            stroke_color = WHITE,
        )
        disk = ParametricSurface(
            lambda u,v: np.array([
                -2,
                u*np.cos(v),
                u*np.sin(v)
            ]),
            u_min = 0,
            u_max = 0.5,
            v_min = 0,
            v_max = 2*np.pi,
            checkerboard_colors = [RED, ORANGE],
            fill_color = WHITE,
            stroke_color = WHITE
        )
        disk2 = ParametricSurface(
            lambda u,v: np.array([
                0,
                u*np.cos(v),
                u*np.sin(v)
            ]),
            u_min = 0,
            u_max = 2.5,
            v_min = 0,
            v_max = 2*np.pi,
            checkerboard_colors = [RED, ORANGE],
            fill_color = WHITE,
            stroke_color = WHITE
        )

        self.play(Write(func), Write(axes))
        self.wait()

        self.play(Transform(func, func2), Write(surface))
        self.wait()

        
        self.move_camera(0.8 * np.pi / 2, -0.45 * np.pi)
        #Rotationskörper
        self.remove(func)
        self.play(
            UpdateFromAlphaFunc(surface, self.update_f),
            rate_func = linear,
            run_time = 2
        )

        #zoom an den Körper
        self.play(Uncreate(axes), surface.center)
        self.wait()
        surface.set_stroke(opacity = 0.5)
        surface.set_fill(opacity = 0.5)
        self.wait()
        for i in range(1,30):
            #if i >= 2:
            #    self.play(*[Uncreate(j) for j in disks[:(i-1)]])
            disks = [
                ParametricSurface(
                    lambda u,v: np.array([
                        u-4,
                        (1/(1+j*6/i))*np.cos(v),
                        (1/(1+j*6/i))*np.sin(v)
                    ]),
                    u_min = 1+j*6/i,
                    u_max = 1+(j+1)*6/i,
                    #u_min = 0,
                    #u_max = 1/(1+j*6/i),
                    v_min = 0,
                    v_max = 2*np.pi,
                    checkerboard_colors = [PURPLE],
                    fill_color = PURPLE,
                    fill_opacity = 0.5,
                    stroke_color = PURPLE,
                    resolution = (1,10),
                ).set_stroke(opacity = 0.5).set_opacity(0.5)
                for j in range (i)
            ]
            self.play(*[Write(j) for j in disks[:i]], run_time = 0.3)
            self.wait(0.3)
            self.play(*[Uncreate(j) for j in disks[:i]], run_time = 0.4)
        
        '''i = 3
        j = 1
        d1 = ParametricSurface(
            lambda u,v: np.array([
                u-4,
                (1/(1+j*6/i))*np.cos(v),
                (1/(1+j*6/i))*np.sin(v)
            ]),
            u_min = 1+j*6/i,
            u_max = 1+(j+1)*6/i,
            #u_min = 0,
            #u_max = 1/(1+j*6/i),
            v_min = 0,
            v_max = 2*np.pi,
            checkerboard_colors = [RED, ORANGE],
            fill_color = WHITE,
            stroke_color = WHITE
        )

        self.play(Write(d1))'''
        
    
    def update_f(self, c, dt):
        a =interpolate(0.1, 2*PI, dt)
        s = ParametricSurface(
            lambda u,v: np.array([
                u,
                (1/u)*np.cos(v),
                (1/u)*np.sin(v)
            ]),
            u_min = 1,
            u_max = 7,
            v_min = 0,
            v_max = a,
            checkerboard_colors = [eval(key) for key in COLOR_MAP.keys()],
            color = YELLOW,
            fill_color = YELLOW
        )
        c.become(s)

class Thumbnail(ThreeDScene):
    def construct(self):
        title = TexMobject("Rotationsvolumen").to_edge(UP)

class Task(Scene):
    def construct(self):
        quote_1 = TextMobject("Betrachtet wird eine große Rotationssymmetrische Schale, die aus")
        quote_2 = TextMobject("einem Steinblock gefertigt wurde. Ein Kubikmeter des Steins hat eine")
        quote_3 = TextMobject("Masse von 2700kg. In einem Koordinatensysten kann ein Querschnitt")
        quote_4 = TextMobject("der Schale mithilfe der Graphen der Funktionen p und q mit")
        f_1_func = TexMobject(r" p\left(x\right)=\sqrt{6x} ")
        f_1_int = TexMobject(r" x \in [0,6] ")
        f_1 = VGroup(f_1_func, f_1_int).arrange_submobjects(RIGHT, buff = 1.4)
        f_2_func = TexMobject(r" q\left(x\right)=\sqrt{4x-8} ")
        f_2_int = TexMobject(r" x \in [2,6] ")
        f_2 = VGroup(f_2_func, f_2_int).arrange_submobjects(RIGHT, buff = 1.4)
        quote_5 = TextMobject("modellhaft dargestellt werden. Dabei beschreibt die x-Achse die")
        quote_6 = TextMobject("Rotationsachse der Schale; eine LE im Koordinatensystem entspricht 1dm")

        quote = VGroup(quote_1,quote_2, quote_3, quote_4, f_1, f_2, quote_5, quote_6).scale(0.8).arrange_submobjects(DOWN, buff = 0.5).to_corner(UP)
        self.play(FadeIn(quote))
        self.wait(2)
        self.play(FadeOut(quote))