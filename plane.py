from shape import Shape
from intersection import Intersection
from ray import Ray
from color import Color
import numpy as np
from constants import EPS
from constants import RAY_MIN_DISTANCE

class Plane(Shape):
    def __init__(self, position: np.ndarray, normal: np.ndarray, color=Color.unnormalized_gray(255)):
        self.position = position
        self.normal = normal
        self.color = color

    def intersection(self, ray: Ray):
        ray_dir_dot_normal = np.dot(ray.direction, self.normal)
        if abs(ray_dir_dot_normal) < EPS:
            return None

        t = np.dot(self.position - ray.origin, self.normal) / ray_dir_dot_normal
        if (t < RAY_MIN_DISTANCE):
            return None
     
        return Intersection(ray, self, t, self.color)