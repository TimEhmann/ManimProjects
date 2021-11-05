from manimlib.imports import *
import numpy as np

class FFFcos(GraphScene,MovingCameraScene):
    CONFIG = {
        "x_min" : -3*np.pi,
        "x_max" : 3*np.pi,
        "x_tick_frequency" : np.pi/2,
        "x_axis_label": "$x$",
        #"x_labeled_nums": np.arange(-3*np.pi,3*np.pi,np.pi/2),
        "y_min" : -5,
        "y_max" : 5,
        "y_tick_frequency" : 1, 
        "y_axis_label": "$y$",
        #"y_labeled_nums": np.arange(-4,4,1),
        "graph_origin": ORIGIN, 
    }
    # Setup the scenes

    def setup(self):            
        GraphScene.setup(self)
        MovingCameraScene.setup(self)

    def construct(self):
        self.setup_axes(animate = True)

        def factorial(n):
            fac = 1
            if n > 0:
                for i in range(1,n+1):
                    fac=fac*i
            return fac

        def taylor_approxmation(k,x):
            value = 0
            for i in range(k):
                value = value + ((x**(2*i)*(-1)**i)/factorial(2*i))
            return value

        def func(x):
            return taylor_approxmation(9,x)
        
        self.play(
            self.camera_frame.scale,.427
        )
        graph = self.get_graph(func)
        graph.set_color(BLUE)

        self.add(graph)
        self.play(ShowCreation(graph), run_time = 3)
        
        self.wait(5)
        self.play(
            self.camera_frame.scale,(1/0.427),
            #self.camera_frame.move_to,dot_at_start_graph
        )
        self.wait()
        self.play(FadeOut(VGroup(*self.mobjects)))
        taylor_series = TextMobject("Taylorreihen").scale(1.5)
        self.play(Write(taylor_series))
        self.wait(4)
        self.play(FadeOutAndShift(taylor_series, DOWN))
        self.wait(5)
