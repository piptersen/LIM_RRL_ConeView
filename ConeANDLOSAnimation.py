from manim import *
import numpy as np
import animationFunctions as aF
import importlib
importlib.reload(aF)

class combScene(ThreeDScene):
    def construct(self):

        # Defines cone shape for animation
        base_radius = 4
        height = 10

        #Defines the number of 'LIM noise' around the base point
        num_points = 5

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

        # Define cone that will 'grow' into (I know it is called initial_cone and so misleading, sorry!)
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
            Transform(initial_cone, cone, replace_mobject_with_target_in_scene = False),
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


        #Creates vectorized mobject group for everything to do with the cone so I can move it easily
        coneGroup = VGroup(cone, initial_cone, dot1, dot2, dot3, small_dots, label, arrow)

        #Defines base circle on the cone
        base_circle = Circle(radius=base_radius, color=BLUE_B, fill_opacity=0.2)
        base_circle.rotate(angle=PI/2, axis=UP)  # Rotate from XY-plane to YZ-plane
        base_circle.move_to(cone.get_start())    # Move to the base of the cone
        base_circle.set_stroke(color=WHITE, width=2)

        #Defines where you want the final circle
        final_circle = base_circle.copy().rotate(-PI/2, axis=UP).move_to(RIGHT * 4).scale(0.6)

        #Creates circle on base of cone
        self.play(Create(base_circle), run_time = 1)
        
        self.wait(1)

        #Make base circle rotate and move to right side
        self.play(Transform(base_circle, final_circle, replace_mobject_with_target_in_scene = True), 
                  coneGroup.animate.scale(0.8).move_to(LEFT*3), run_time = 2)


        #Defines location of points in the new LOS circle from the location on the cone
        projected_dot1 = Dot(
            aF.point_on_circle(1/5, np.pi/4, 4*0.6)+ base_circle.get_center(),
            color=BLUE_C
        )
        projected_dot2 = Dot(
            aF.point_on_circle(2/3, np.pi/4, 4*0.6)+ base_circle.get_center(),
            color=ORANGE
        )

        projected_dot3 = Dot(
            aF.point_on_circle(np.sqrt(2)/5, np.pi/4, 4*0.6)+ base_circle.get_center(),
            color=BLUE_C
        )


        #Defines the 'LIM Noise' points around the emission point for the LOS circle
        projected_small_dots = VGroup()
        for i in range(num_points):
            pos = projected_dot1.get_center() + [0.3*np.sin(thetas[i]), 0.3*np.cos(thetas[i]), 0]
            pos2 = projected_dot2.get_center() + [0.3*np.sin(thetas[i]), 0.3*np.cos(thetas[i]), 0]
            pos3 = projected_dot3.get_center() + [0.3*np.sin(thetas[i]), 0.3*np.cos(thetas[i]), 0]
            
            projected_small_dots.add(Dot(pos, radius=0.05, color=BLUE_B))
            projected_small_dots.add(Dot(pos2, radius=0.05, color=ORANGE))
            projected_small_dots.add(Dot(pos3, radius=0.05, color=BLUE_B))


        #Adds all the points in the new LOS circle
        self.play(
            FadeIn(projected_dot1),
            FadeIn(projected_dot2),
            FadeIn(projected_dot3),
            FadeIn(projected_small_dots),
            run_time=1
        )

        
        self.wait(3)


        #Adds all the newly 'observed' points to both the cone and LOS circle
        points_data = aF.generate_cone_points(10)
        for i, point_pos in enumerate(points_data):
            #Generates cone point location and LOS point location
            cone_pt = aF.point_on_cone(*point_pos, cone_length=10*0.6, cone_radius=4*0.6)
            proj_pt = base_circle.get_center() + aF.point_on_circle(*point_pos, base_radius*0.6)
            surr_pts = VGroup()
            
            for j in range(num_points):
                #Generates the 'LIM Noise' points for each cone and LOS point
                fuzz_pt = proj_pt + [0.3*np.sin(thetas[j]), 0.3*np.cos(thetas[j]), 0]
                surr_pts.add(Dot(fuzz_pt, radius = 0.05, color = ORANGE))
                surr_pts.add(Dot3D(cone_pt+[0,0.3*np.cos(thetas[j]),0.3*np.sin(thetas[j])], radius=0.05, color=ORANGE))

            #Adds all the points to the scene
            self.add(Dot3D(point = cone_pt, color = ORANGE), Dot(point = proj_pt, color = ORANGE), surr_pts)
            self.wait(1)

        self.wait(5)