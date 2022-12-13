from ray import Ray

import numpy as np
import math

class Camera:
    def __init__(self, position: np.ndarray, target: np.ndarray, up_guide: np.ndarray, 
                 fov: float, aspect_ratio: float):
        self.position = position
        
        self.forward = (target - position)
        self.forward = self.forward / np.linalg.norm(self.forward)
        
        self.right = np.cross(self.forward, up_guide)
        self.right = self.right / np.linalg.norm(self.right)

        self.up = np.cross(self.right, self.forward)
        self.h = math.tan(fov)
        self.w = self.h * aspect_ratio

    def make_ray(self, x, y):
        direction = self.forward + (x * self.w * self.right + y * self.h * self.up)
        direction = direction / np.linalg.norm(direction)
        return Ray(self.position, direction)