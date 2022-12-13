import numpy as np
import PIL as pil
from PIL import Image as PILImage

class Image:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.data = np.zeros((self.height, self.width, 3))
    
    def put_pixel(self, x: int, y: int, color = [255, 255, 255]):
        if (x < 0 or x >= self.width):
            raise ValueError("Invalid x")
        if (y < 0 or y >= self.height):
            raise ValueError("Invalid y")

        self.data[y, x] = color

    def save(self, filename):
        print(self.data.shape)
        img = PILImage.fromarray(np.uint8(self.data))
        img.save(filename)