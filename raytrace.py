from scene import Scene
from image import Image
from camera import Camera

import numpy as np
import math

def ray_trace(image: Image, scene: Scene, camera: Camera):
    for x in range(image.width):
        for y in range(image.height):
            camera_x = 2.0 * x / image.width - 1.0
            camera_y = -2.0 * y / image.height + 1.0
            ray = camera.make_ray(camera_x, camera_y)
            color = scene.cast_ray(ray)
            if color is not None:
                image.put_pixel(x, y, color)
