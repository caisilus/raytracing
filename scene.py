from intersection import Intersection
from ray import Ray
from shape import Shape

from typing import List

class Scene:
    shapes: List[Shape]
    
    def __init__(self):
        self.shapes = []

    def add_shape(self, shape: Shape):
        self.shapes.append(shape)

    def cast_ray(self, ray: Ray) -> Intersection:
        intersection = Intersection(ray)
        for shape in self.shapes:
            shape_intersection = shape.intersection(ray)
            if shape_intersection is None:
                continue
            if shape_intersection < intersection:
                intersection = shape_intersection
        
        if intersection.t == ray.max_t:
            return None
        return intersection

    def does_intesect(self, intersection: Intersection):
        for shape in self.shapes:
            if shape.intersect(intersection):
                return True
        return False