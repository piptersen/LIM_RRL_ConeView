from manim import *
import numpy as np

class JumpingParabolas(Scene):
    def construct(self):

        n_obs = 10
        #Defines the coordinate system
        axes = Axes(
            x_range=[0, 10],
            y_range=[0, 6],
            x_length=10,
            y_length=6,
        )

        #Defines labels of coordinate system
        labels = axes.get_axis_labels(
            Text("").scale(0.45), Text("Power Spectrum").scale(0.45)
        )

        #Adds coordsystem and label to scene
        self.add(axes, labels)
        
        self.wait(6)

        #Generates 21cm curve
        def rrl_curve(x):
            return -(x-5)**2 / 15 + 5
        base_curve = axes.plot(rrl_curve, color=BLUE)
        

        # Label for both curves
        label_21cm = Text("21cm Auto PS", color=BLUE).scale(0.5).to_corner(UR).shift(DOWN * 0.5)
        label_rrl = Text("RRL Auto PS", color=ORANGE).scale(0.5).next_to(label_21cm, DOWN, aligned_edge=RIGHT)
        label_rrlCross = Text("RRL-21 Cross PS (Effect)", color=GREEN).scale(0.5).next_to(label_rrl, DOWN, aligned_edge=RIGHT)

        
        # Animate RRL curve jumping up with observation
        for i in range(1, (n_obs+2)):
            #How much line should jump by
            alpha = 1.6 + i * 0.1

            # Line to jump
            def updated_curve(x, a=alpha):
                return -(x-5)**2 / 15 + a
            new_curve = axes.plot(lambda x: updated_curve(x), color=ORANGE)


            if i == 1:
                #As a first step, add in the RRL curve, the 21cm curve, and all the labels
                self.play(FadeIn(new_curve), FadeIn(base_curve), FadeIn(label_21cm), FadeIn(label_rrl), FadeIn(label_rrlCross), run_time = 2)
                self.wait(4)
            else:
                self.add(new_curve)
                
            if i == 6:
                #Hard coded version of which point is 'close enough' from previous animation to contaminate
                self.add(axes.plot(lambda x: (-190*alpha*(x-2.45)*(x-2.68)*(x-2.85)*(x-3.3)*(x-3.7)*(x-3.4)) if x > 2.2 and x < 3.6 else -10, color=GREEN))
                
            if i == 11:
                #Hard coded version of which point is 'close enough' from previous animation to contaminate
                self.add(axes.plot(lambda x: (-220*alpha*(x-2.7)*(x-2.93)*(x-3.1)*(x-3.55)*(x-3.85)*(x-4)) if x > 2.45 and x < 4.2 else -10, color=GREEN))
                
            self.wait(1)
            
            if i < (n_obs+1):
                self.remove(new_curve)
                
        self.wait(5)