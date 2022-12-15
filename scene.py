from intersection import Intersection
from ray import Ray
from shape import Shape
from point_light import PointLight
from vector_helpers import normalize
from color import Color
from constants import EPS

from typing import List

import numpy as np

class Scene:
    shapes: List[Shape]
    
    def __init__(self, max_depth = 1, shadow_brightness = 0.0):
        self.max_depth = max_depth
        self.shadow_brightness = shadow_brightness
        self.shapes = []

    def add_shape(self, shape: Shape):
        self.shapes.append(shape)

    def add_light_source(self, light_source: PointLight):
        self.light_source = light_source

    def cast_ray(self, ray: Ray) -> Color:
        # nearest_intersection = self.nearest_intersection(ray)
        # if nearest_intersection is None:
        #     return None

        # illumination = np.array([self.shadow_brightness, self.shadow_brightness, self.shadow_brightness])
        # if self.check_light(nearest_intersection):
        #     illumination = self.calculate_illumination(ray, nearest_intersection)

        illumination = self.sum_illumination(ray)

        color = Color.from_array(np.clip(illumination, 0.0, 1.0))
        return color

    def sum_illumination(self, ray: Ray, depth=0):
        nearest_intersection = self.nearest_intersection(ray)
        if nearest_intersection is None:
            return np.zeros((3))
    
        illumination = self.calculate_illumination(ray, nearest_intersection)

        reflection = nearest_intersection.material().reflection

        if (depth == self.max_depth) or (reflection < EPS):
            return illumination

        reflected_ray = self.reflected(ray, nearest_intersection)
        return illumination + reflection * self.sum_illumination(reflected_ray, depth + 1)

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
        
        if not self.check_light(intersection):
            return ambient
        
        # diffuse
        diffuse = (material.diffuse_color * self.light_source.diffuse_color).data 
        diffuse *= np.dot(direction_to_light, normal)
        # specular
        h = normalize(direction_to_light + direction_to_camera)
        specular = (material.specular_color * self.light_source.specular_color).data
        specular *= np.dot(normal, h) ** (material.shininess / 4.0)

        illumination = ambient + diffuse + specular
        return illumination

    def reflected(self, ray: Ray, intersection: Intersection):
        normal = intersection.normal()
        reflected_ray_origin = intersection.position() + 1e-5 * normal
        reflected_ray_direction = ray.direction - 2 * np.dot(ray.direction, normal) * normal
        return Ray(reflected_ray_origin, reflected_ray_direction)

    def does_intesect(self, intersection: Intersection):
        for shape in self.shapes:
            if shape.intersect(intersection):
                return True
        return False