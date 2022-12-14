from material import Material
import numpy as np

class PointLight:
    def __init__(self, position: np.ndarray, material: Material):
        self.position = position
        self.ambient_color = material.ambient_color
        self.diffuse_color = material.diffuse_color
        self.specular_color = material.specular_color