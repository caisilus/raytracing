from intersection import Intersection
from ray import Ray

class Shape:
    def intersection(self, ray: Ray) -> Intersection:
        raise NotImplementedError("Intersect is not implemented")
