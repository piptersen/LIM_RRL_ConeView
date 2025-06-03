from manim import *
import numpy as np
import animationFunctions as aF
import importlib
importlib.reload(aF)


#Makes the animation output a square in the config file
config = {
    "frame_width": 10.0,
    "frame_height": 10.0,
    "pixel_width": 1920,
    "pixel_height": 1920,
}


class CircleViewScene(Scene):
    def construct(self):

        #Defines cone shape for animation (I have it as 3.9 not 4 because 4 gets cut off in this case!
        circle_radius = 3.9

        #Defines the number of 'LIM noise' around the base point
        num_points = 5

        #Defines number of observations to add
        n_obs = 10

        
        #Defines circle shape
        circle = Circle(radius=circle_radius, color=BLUE_B, fill_opacity=0.2)

        #Creates the base circle
        self.play(DrawBorderThenFill(circle), run_time = 4)


        #Defines Initial 3 emission dots
        dot1_pos = aF.cone_point_to_circle(1/5, circle_radius = circle_radius)
        dot2_pos = aF.cone_point_to_circle(2/3, circle_radius = circle_radius)
        dot3_pos = dot1_pos + [-0.3, -0.3, 0]

        dot1 = Dot(dot1_pos, color=BLUE_C)
        dot2 = Dot(dot2_pos, color=ORANGE)
        dot3 = Dot(dot3_pos, color=BLUE_C)


        #Defines the 'LIM Noise' points
        thetas = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
        projected_small_dots = VGroup()
        for i in range(num_points):
            pos = dot1.get_center() + [0.3*np.sin(thetas[i]), 0.3*np.cos(thetas[i]), 0]
            pos2 = dot2.get_center() + [0.3*np.sin(thetas[i]), 0.3*np.cos(thetas[i]), 0]
            pos3 = dot3.get_center() + [0.3*np.sin(thetas[i]), 0.3*np.cos(thetas[i]), 0]
            
            projected_small_dots.add(Dot(pos, radius=0.05, color=BLUE_B))
            projected_small_dots.add(Dot(pos2, radius=0.05, color=ORANGE))
            projected_small_dots.add(Dot(pos3, radius=0.05, color=BLUE_B))

        
        #Defines reference dots (for label)
        ref_dot1 = Dot(color=BLUE_C).scale(0.7).to_corner(UL).shift(DOWN * 0.1 + RIGHT * 0.1)
        ref_label1 = Text("21cm Emission", font_size=20).next_to(ref_dot1, RIGHT, buff=0.2)
        ref_dot2 = Dot(color=ORANGE).scale(0.7).next_to(ref_dot1, DOWN, buff=0.4)
        ref_label2 = Text("RRL Emission", font_size=20).next_to(ref_dot2, RIGHT, buff=0.2)

        
        self.wait(2)

        #Create initial emission dots and labels
        self.play(FadeIn(dot1), 
                  FadeIn(dot2), 
                  FadeIn(dot3), 
                  FadeIn(projected_small_dots), 
                  FadeIn(VGroup(ref_dot1, ref_label1, ref_dot2, ref_label2)),
                  run_time=2
                 )

        
        self.wait(5)

        #Adds all the newly 'observed' points the LOS circle
        points_data = aF.generate_cone_points(n_obs)
        for i, point_pos in enumerate(points_data):
            #Generates observation points on the circle
            proj_pt = circle.get_center() + aF.point_on_circle(*point_pos)
            surr_pts = VGroup()
            
            for j in range(num_points):
                #Generates the 'LIM Noise' points for each cone and LOS point
                fuzz_pt = proj_pt + [0.3*np.sin(thetas[j]), 0.3*np.cos(thetas[j]), 0]
                surr_pts.add(Dot(fuzz_pt, radius = 0.05, color = GREEN if (i == 4 or i == 9) else ORANGE))
            
            #Adds all the points to the scene
            self.add(Dot(point = proj_pt, color = GREEN if (i == 4 or i == 9) else ORANGE), surr_pts)
            self.wait(1)

        self.wait(5)