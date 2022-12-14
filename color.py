import numpy as np
import math

class Color():
    def __init__(self, r = 0, g = 0, b = 0):
        self.data = np.array([r, g, b])

    def from_array(array):
        r, g, b = array[0], array[1], array[2]
        return Color(r, g, b)

    def gray(w):
        return Color(w, w, w)

    def unnormalized_gray(w):
        normalized_w = w / 255
        return Color(normalized_w, normalized_w, normalized_w)

    # r, g, b from 0 to 255
    def unnormalized(r, g, b):
        return Color(r / 255, g / 255, b / 255)

    def clamp(self, min = 0.0, max = 1.0):
        return np.clip(self.data, min, max)

    def __add__(self, other):
        if not isinstance(other, Color):
            raise TypeError("Cannot add color with not color")

        return Color.from_array(self.data + other.data)

    def __mul__(self, other):
        if not isinstance(other, Color):
            raise TypeError("Cannot multiply color with not color")

        return Color.from_array(self.data * other.data)
        
    def red(r=1.0):
        return Color(r, 0.0, 0.0)

    def green(g=1.0):
        return Color(0.0, g, 0.0)

    def blue(b=1.0):
        return Color(0.0, 0.0, b)

    def yellow(y=1.0):
        return Color(y, y, 0.0)

    def purple(p=1.0):
        return Color(p, 0.0, p)

    def turquoise(t=1.0):
        return Color(0.0, t, t)
