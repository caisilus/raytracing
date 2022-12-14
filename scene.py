from intersection import Intersection
from ray import Ray
from shape import Shape
from point_light import PointLight
from vector_helpers import normalize
from color import Color

from typing import List

import numpy as np

class Scene:
    shapes: List[Shape]
    
    def __init__(self):
        self.shapes = []

    def add_shape(self, shape: Shape):
        self.shapes.append(shape)

    def add_light_source(self, light_source: PointLight):
        self.light_source = light_source

    def cast_ray(self, ray: Ray) -> Color:
        nearest_intersection = self.nearest_intersection(ray)
        if nearest_intersection is None:
            return None
        illumination = self.calculate_illumination(ray, nearest_intersection)
        color = Color.from_array(np.clip(illumination, 0, 1))
        return color

    def nearest_intersection(self, ray: Ray):
        intersection = Intersection(ray)
        for shape in self.shapes:
            shape_intersection = shape.intersection(ray)
            if shape_intersection is None:
                continue
            if shape_intersection < intersection:
                intersection = shape_intersection
        
        if (intersection.t == ray.max_t) or (intersection.intersected_shape is None):
            return None

        return intersection

    def calculate_illumination(self, ray: Ray, intersection: Intersection):
        direction_to_light = normalize(self.light_source.position - intersection.position())
        direction_to_camera = normalize(-ray.direction)
        # normal = intersection.shape.normal_at_point(intersection.position)
        normal = intersection.normal()

        # material = intersection.shape.material
        material = intersection.material()
        illumination = np.zeros((3))
        # ambient
        ambient = (material.ambient_color * self.light_source.ambient_color).data
        # diffuse
        diffuse = (material.diffuse_color * self.light_source.diffuse_color).data 
        diffuse *= np.dot(direction_to_light, normal)
        # specular
        h = normalize(direction_to_light + direction_to_camera)
        specular = (material.specular_color * self.light_source.specular_color).data
        specular *= np.dot(normal, h) ** (material.shininess / 4.0)

        illumination = ambient + diffuse + specular
        return illumination

    def does_intesect(self, intersection: Intersection):
        for shape in self.shapes:
            if shape.intersect(intersection):
                return True
        return False