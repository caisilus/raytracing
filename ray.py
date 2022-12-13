import numpy as np
from constants import RAY_MIN_DISTANCE, RAY_MAX_DISTANCE 

class Ray:
    def __init__(self, origin: np.ndarray, direction: np.ndarray, max_t = RAY_MAX_DISTANCE):
        self.origin = origin
        self.direction = direction
        self.max_t = max_t

    def ray_point(self, t: float):
        return self.origin + self.direction * t

    def copy(ray):
        return Ray(np.copy(ray.origin), np.copy(ray.direction), ray.max_t)