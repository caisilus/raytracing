from shape import Shape
from ray import Ray
from intersection import Intersection
from constants import RAY_MIN_DISTANCE, EPS
from vector_helpers import normalize
import numpy as np

class Box(Shape):
    def __init__(self, center: np.ndarray, size_x, size_y, size_z, box_material):
        self.center = center
        self.sizes = np.array([size_x, size_y, size_z])
        self.left_bottom_corner = np.array([-size_x / 2, -size_y / 2, -size_z / 2])
        self.right_up_corner = np.array([size_x / 2, size_y / 2, size_z / 2])
        super().__init__(box_material)
    
    def intersection(self, ray: Ray) -> Intersection:
        local_ray = self.translated_ray(ray)
        tmin = (self.left_bottom_corner[0] - local_ray.origin[0]) / local_ray.direction[0]
        tmax = (self.right_up_corner[0] - local_ray.origin[0]) / local_ray.direction[0]

        if tmin > tmax:
            tmin, tmax = tmax, tmin
        
        tymin = (self.left_bottom_corner[1] - local_ray.origin[1]) / local_ray.direction[1]
        tymax = (self.right_up_corner[1] - local_ray.origin[1]) / local_ray.direction[1]

        if tymin > tymax:
            tymin, tymax = tymax, tymin

        if ((tmin > tymax) or (tymin > tmax)): 
            return None

        if (tymin > tmin): 
            tmin = tymin
    
        if (tymax < tmax):
            tmax = tymax

        tzmin = (self.left_bottom_corner[2] - local_ray.origin[2]) / local_ray.direction[2]
        tzmax = (self.right_up_corner[2] - local_ray.origin[2]) / local_ray.direction[2]

        if (tzmin > tzmax):
            tzmin, tzmax = tzmax, tzmin 
    
        if ((tmin > tzmax) or (tzmin > tmax)):
            return None 
    
        if (tzmin > tmin):
            tmin = tzmin
    
        if (tzmax < tmax): 
            tmax = tzmax

        if tmin >= tmax:
            return None

        if tmin > RAY_MIN_DISTANCE:
            return Intersection(ray, self, tmin)
        if tmax > RAY_MIN_DISTANCE:
            return Intersection(ray, self, tmax)
        
        return None

    def translated_ray(self, ray: Ray):
        translated_ray = Ray.copy(ray)
        translated_ray.origin = translated_ray.origin - self.center
        return translated_ray

    def step(self, edge: np.ndarray, vec: np.ndarray):
        return (vec >= edge) * 1.0

    def normal_at_point(self, point: np.ndarray):
        translated_point = point - self.center
        normal_dec = np.abs(translated_point) / self.sizes
        max_coordinate = np.max(normal_dec)
        
        normal_dec = normal_dec * (np.abs(normal_dec) >= max_coordinate)
        
        normal = normal_dec * translated_point
        normal = normalize(normal)
        return normal

    def check_cached(self, point: np.ndarray):
        return np.min(np.abs(self.cached_point - point) < EPS)