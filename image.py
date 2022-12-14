from color import Color

import numpy as np
import PIL as pil
from PIL import Image as PILImage

class Image:
    def __init__(self, width: int, height: int, apply_gamma_correction = True):
        self.width = width
        self.height = height
        self.data = np.zeros((self.height, self.width, 3))
    
    def put_pixel(self, x: int, y: int, color: Color):
        if (x < 0 or x >= self.width):
            raise ValueError("Invalid x")
        if (y < 0 or y >= self.height):
            raise ValueError("Invalid y")

        self.data[y, x] = color.data

    def apply_gamma_correction(self, exposure, gamma):
        return np.clip(np.power(self.data * exposure, gamma), 0.0, 1.0)

    def save(self, filename, apply_gamma_correction=False, exposure = 1.0, gamma = 2.2):
        if apply_gamma_correction:
            data = self.apply_gamma_correction(exposure, gamma)
        else:
            data = self.data
        img = PILImage.fromarray(np.uint8(data * 255))
        img.save(filename)