from shape import Shape
from intersection import Intersection
from ray import Ray
from material import Material
import numpy as np
from constants import EPS
from constants import RAY_MIN_DISTANCE
from vector_helpers import normalize

class Plane(Shape):
    def __init__(self, position: np.ndarray, normal: np.ndarray, material: Material):
        self.position = position
        self.normal = normal
        super().__init__(material)

    def intersection(self, ray: Ray):
        ray_dir_dot_normal = np.dot(ray.direction, self.normal)
        if abs(ray_dir_dot_normal) < EPS:
            return None

        t = np.dot(self.position - ray.origin, self.normal) / ray_dir_dot_normal
        if (t < RAY_MIN_DISTANCE):
            return None
     
        return Intersection(ray, self, t)

    def normal_at_point(self, point: np.ndarray):
        return normalize(self.normal)