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
    
    def __init__(self, max_depth = 2):
        self.max_depth = max_depth
        self.shapes = []

    def add_shape(self, shape: Shape):
        self.shapes.append(shape)

    def add_light_source(self, light_source: PointLight):
        self.light_source = light_source

    def cast_ray(self, ray: Ray, shadow_brightness=0.1, depth=0) -> Color:
        nearest_intersection = self.nearest_intersection(ray)
        if nearest_intersection is None:
            return None

        illumination = np.array([shadow_brightness, shadow_brightness, shadow_brightness])
        if self.check_light(nearest_intersection):
            illumination = self.calculate_illumination(ray, nearest_intersection)
        
        color = Color.from_array(np.clip(illumination, 0.0, 1.0))
        return color

    def nearest_intersection(self, ray: Ray):
        intersection = Intersection(ray)
        for shape in self.shapes:
            shape_intersection = shape.intersection(ray)
            if shape_intersection is None:
                continue
            if shape_intersection < intersection:
                intersection = shape_intersection
        
        if self.no_intersection(intersection, ray):
            return None

        return intersection

    def no_intersection(self, intersection, ray):
        return (intersection.t == ray.max_t) or (intersection.intersected_shape is None)

    def check_light(self, intersection):
        ray = self.ray_to_light(intersection)
        distance_to_light = self.distance_to_light(ray.origin)
        nearest_intersection = self.nearest_intersection(ray)
        return self.no_intersection(nearest_intersection, ray) or (nearest_intersection.t > distance_to_light) 

    def distance_to_light(self, position: np.ndarray):
        direction_to_light = self.light_source.position - position
        return np.linalg.norm(direction_to_light)

    def ray_to_light(self, intersection):
        pos = intersection.position()
        origin = pos + 1e-5 * intersection.normal()
        direction = self.light_source.position - origin
        return Ray(origin, direction)

    def calculate_illumination(self, ray: Ray, intersection: Intersection):
        direction_to_light = normalize(self.light_source.position - intersection.position())
        direction_to_camera = normalize(-ray.direction)
        
        normal = intersection.normal()
        material = intersection.material()
        
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

    def reflected(ray: Ray, intersection: Intersection):
        reflected_ray_origin = intersection.position()
        normal = intersection.normal()
        reflected_ray_direction = ray.direction - 2 * np.dot(ray.direction, normal) * normal
        return Ray(reflected_ray_origin, reflected_ray_direction)

    def does_intesect(self, intersection: Intersection):
        for shape in self.shapes:
            if shape.intersect(intersection):
                return True
        return False