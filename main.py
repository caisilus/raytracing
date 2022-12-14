from camera import Camera
from scene import Scene
from sphere import Sphere
from plane import Plane
from image import Image
from color import Color

import numpy as np
import math

from raytrace import ray_trace

scene = Scene()
scene.add_shape(Plane(np.array([0.0, 0.0, 0.0]), np.array([0.0, 1.0, 0.0]), Color(0.5, 0.5, 0.5)))
scene.add_shape(Sphere(np.array([0, 1.0, 0]), 1.0, Color.blue()))

image = Image(1920, 1080)
camera = Camera(np.array([-5.0, 1.0, 0.0]), np.array([0.0, 1.0, 0.0]), 
                np.array([0.0, 1.0, 0.0]), 25 * math.pi / 180.0, image.width / image.height)

ray_trace(image, scene, camera)
image.save("output.jpg")
image.save("gamma_corrected.jpg", True)