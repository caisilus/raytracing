from ray import Ray
from vector_helpers import normalize

import numpy as np
import math

class Camera:
    def __init__(self, position: np.ndarray, target: np.ndarray, up_guide: np.ndarray, 
                 fov: float, aspect_ratio: float):
        self.position = position
        
        self.forward = normalize(target - position)
        
        self.right = normalize(np.cross(self.forward, up_guide))
        
        self.up = np.cross(self.right, self.forward)
        self.h = math.tan(fov)
        self.w = self.h * aspect_ratio

    def make_ray(self, x, y):
        direction = self.forward + (x * self.w * self.right + y * self.h * self.up)
        direction = direction / np.linalg.norm(direction)
        return Ray(self.position, direction)