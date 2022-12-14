from intersection import Intersection
from ray import Ray
from material import Material
import numpy as np

class Shape:
    def __init__(self, material):
        self.material = material

    def intersection(self, ray: Ray) -> Intersection:
        raise NotImplementedError("Intersect is not implemented")

    def normal_at_point(self, point: np.ndarray):
        raise NotImplementedError("Normal at point is not implemented")
