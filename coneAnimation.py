from manim import *
import numpy as np
import animationFunctions as aF
import importlib
importlib.reload(aF)

class LCScene(ThreeDScene):
    def construct(self):

        #Defines cone shape for animation
        base_radius = 4
        height = 10

        #Defines the number of 'LIM noise' around the base point
        num_points = 5

        #Defines number of observations to add
        n_obs = 10

        #Initializes cones
        cone = Cone(
            base_radius=base_radius,
            height=height,
            direction=-X_AXIS,
            fill_opacity=0.15,
            fill_color=BLUE_B,
            stroke_width=0,
            resolution=(6, 16), 
        ).shift(LEFT * 6)

        #Adds the initial cone so it starts on the screen
        self.add(cone)

        
        #Define cone that will 'grow' into (I know it is called initial_cone and so misleading, sorry!)
        initial_cone = Cone(
            base_radius=0.01,
            height=0.01,
            direction=-X_AXIS,
            fill_opacity=0.15,
            fill_color=BLUE_A,
            stroke_width=0,
            resolution=(6, 16),
        ).shift(LEFT * 6)

        
        #Defines Initial 3 emission dots
        dot1 = Dot3D(aF.point_along_cone(1/5), color=BLUE_C)
        dot2 = Dot3D(aF.point_along_cone(2/3), color=ORANGE)
        dot3 = Dot3D(aF.point_along_cone(1/5)+[0, -0.75, -0.75], color=BLUE_C)

        
        dot1_pos = dot1.get_center()
        dot3_pos = dot3.get_center()

        #Defines reference dots (for label)
        ref_dot1 = Dot(color=BLUE_C).scale(0.7).to_corner(UL).shift(DOWN * 0.1 + RIGHT * 0.1)
        ref_label1 = Text("21cm Emission", font_size=20).next_to(ref_dot1, RIGHT, buff=0.2)
        
        ref_dot2 = Dot(color=ORANGE).scale(0.7).next_to(ref_dot1, DOWN, buff = 0.4)
        ref_label2 = Text("RRL Emission", font_size=20).next_to(ref_dot2, RIGHT, buff = 0.2)

        
        # Create a redshift label and arrow above the cone
        label = Text("Redshift", font_size=24).move_to(UP * 3.5)
        arrow = Arrow(
            start=LEFT * 3 + UP * 3,
            end=RIGHT * 3 + UP * 3,
            buff=0,
            stroke_width=4,
            color=RED
        )


        #Defines the 'LIM Noise' points
        thetas = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
        small_dots = VGroup()
        
        for theta in thetas:
            pos = dot1.get_center() + [0,0.3*np.cos(theta),0.3*np.sin(theta)]
            pos2 = dot2.get_center() + [0,0.3*np.cos(theta),0.3*np.sin(theta)]
            pos3 = dot3.get_center() + [0,0.3*np.cos(theta),0.3*np.sin(theta)]
            small_dots.add(Dot3D(pos, radius=0.05, color=BLUE_B), Dot3D(pos2, radius=0.05, color=ORANGE), Dot3D(pos3, radius=0.05, color=BLUE_B))


        #Begin cone animation
        self.add(initial_cone)
        self.play(
            Transform(initial_cone, cone),
            GrowArrow(arrow), 
            FadeIn(label),
            run_time=5
        )
        
        self.wait(1)

        #Create initial emission dots and labels
        self.play(
            FadeIn(dot1),
            FadeIn(dot2),
            FadeIn(dot3),
            FadeIn(small_dots),
            FadeIn(VGroup(ref_dot1, ref_label1, ref_dot2, ref_label2)),
            run_time=2
        )
        
        self.wait(5)

        #Adds all the newly 'observed' points the cone
        close_enough = 1.65
        points_data = aF.generate_cone_points(n_obs)
        for i, point_pos in enumerate(points_data):
            #Generates more observation points on the cone
            cone_pt = aF.point_on_cone(*point_pos, cone_length=10, cone_radius=4)
            surr_pts = VGroup()
            
            for j in range(num_points):
                #Generates the 'LIM Noise' around each cone point, and checks if they are 'close enough' to contaminate physical space
                surr_pts.add(Dot3D(cone_pt+[0,0.3*np.cos(thetas[j]),0.3*np.sin(thetas[j])], radius=0.05, color=GREEN_C if ((np.linalg.norm(cone_pt - dot1_pos) <= close_enough) or (np.linalg.norm(cone_pt - dot3_pos) <= close_enough)) else ORANGE))
            
            #Adds all the points to the scene
            self.add(Dot3D(point = cone_pt, color=GREEN_C if ((np.linalg.norm(cone_pt - dot1_pos) <= close_enough) or (np.linalg.norm(cone_pt - dot3_pos) <= close_enough)) else ORANGE), surr_pts)
            self.wait(1)

        self.wait(5)