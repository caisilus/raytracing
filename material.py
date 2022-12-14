from color import Color
import numpy as np

class Material:
    def __init__(self, ambient_color: Color, diffuse_color: Color, specular_color: Color, 
                       shininess: float = 100.0):
        self.ambient_color = ambient_color
        self.diffuse_color = diffuse_color
        self.specular_color = specular_color
        self.shininess = shininess