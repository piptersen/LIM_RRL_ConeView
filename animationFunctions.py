import numpy as np
from manim import *

def generate_cone_points(n_points, seed=3, max_fraction=1.0):
    np.random.seed(seed)
    rs = np.sqrt(np.random.uniform(0, max_fraction**2, size=n_points))  # uniform in area
    thetas = np.random.uniform(0, 2 * np.pi, size=n_points)
    return list(zip(rs, thetas))
    
def point_on_cone(r_frac, theta, cone_length=10, cone_radius=4, radius_buffer_frac=0.9):
    # Move along the cone axis from tip (-6) to base (+4)
    x = -6 + r_frac * cone_length  # x ranges from -6 to +4

    # Maximum possible radius at this x position
    max_radius = r_frac * cone_radius

    # Shrink the actual radius to stay inside the cone
    radius = radius_buffer_frac * max_radius

    y = radius * np.cos(theta)
    z = radius * np.sin(theta)
    return np.array([x, y, z])
    

def point_on_circle(r_frac, theta, circle_radius=4):
    r = r_frac * circle_radius
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return np.array([x, y, 0])

def point_along_cone(fraction, height = 10, base_radius = 4):
        """Get a point along the axis of the cone and spread it out"""
        axis_point = LEFT * 3 + RIGHT * height * fraction
        radius = base_radius * fraction
        return axis_point + UP * (radius * 0.5) + OUT * (radius * 0.5)

def cone_point_to_circle(fraction, circle_radius = 4):
        r = circle_radius * fraction
        return np.array([r * 0.5, r * 0.5, 0])  # Approximate projection