import numpy as np
import math

class Color():
    def __init__(self, r = 0, g = 0, b = 0):
        self.r = r
        self.g = g
        self.b = b

    def gray(w):
        return Color(w, w, w)

    def unnormalized_gray(w):
        normalized_w = w / 255
        return Color(normalized_w, normalized_w, normalized_w)

    # r, g, b from 0 to 255
    def unnormalized(r, g, b):
        return Color(r / 255, g / 255, b / 255)

    def clamp(self, min = 0.0, max = 1.0):
        self.r = self.clamp_component(self.r, min, max)
        self.g = self.clamp_component(self.g, min, max)
        self.b = self.clamp_component(self.b, min, max)

    def clamp_component(self, component, min, max):
        component = math.min(max, component)
        component = math.max(min, component)
        return component

    def to_nparray(self):
        return np.array([self.r, self.g, self.b])

    def __add__(self, other):
        if not isinstance(other, Color):
            raise TypeError("Cannot add color with not color")

        return Color(self.r + other.r, self.g + other.g, self.b + other.b)

    def __mul__(self, other):
        if not isinstance(other, Color):
            raise TypeError("Cannot multiply color with not color")

        return Color(self.r * other.r, self.g * other.g, self.b * other.b)
        
    def red():
        return Color(1.0, 0.0, 0.0)

    def green():
        return Color(0.0, 1.0, 0.0)

    def blue():
        return Color(0.0, 0.0, 1.0)
