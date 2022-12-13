from shape import Shape
from ray import Ray
from constants import RAY_MIN_DISTANCE
from intersection import Intersection

import numpy as np
import math

class Sphere(Shape):
    def __init__(self, center: np.ndarray, radius: float):
        self.center = center
        self.radius = radius

    def intersection(self, ray: Ray):
        local_ray = self.translated_ray(ray)
        a = np.linalg.norm(local_ray.direction) ** 2
        b = 2 * np.dot(local_ray.direction, local_ray.origin)
        c = np.linalg.norm(local_ray.origin) ** 2 - self.radius ** 2
        ts = self.quadric_equation_solution(a, b, c)
        t = self.best_solution(ts)
        if t is None:
            return None
        return Intersection(ray, self, t)

    def quadric_equation_solution(self, a, b, c):
        discriminant = b ** 2 - 4 * a * c
        if discriminant < 0:
            return []
        
        t1 = (-b - math.sqrt(discriminant)) / (2 * a)
        t2 = (-b + math.sqrt(discriminant)) / (2 * a)
        if (t1 == t2):
            return [t1]
        
        return [t1, t2]


    def best_solution(self, ts):
        if len(ts) == 0:
            return None
        
        if len(ts) == 1:
            if ts[0] > RAY_MIN_DISTANCE:
                return ts[0]
            return None

        t1, t2 = sorted(ts)
        if t1 > RAY_MIN_DISTANCE:
            return t1
        if t2 > RAY_MIN_DISTANCE:
            return t2
        return None


    def translated_ray(self, ray: Ray):
        translated_ray = Ray.copy(ray)
        translated_ray.origin = translated_ray.origin - self.center
        return translated_ray