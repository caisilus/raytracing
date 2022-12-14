from camera import Camera
from scene import Scene
from sphere import Sphere
from plane import Plane
from image import Image
from color import Color
from material import Material
from point_light import PointLight

import numpy as np
import math

from raytrace import ray_trace

scene = Scene()

sphere_material = Material(Color(0.1, 0, 0), Color(0.7, 0, 0), Color.gray(1.0))
plane_material = Material(Color.gray(0.1), Color.gray(0.5), Color.gray(1.0), 0.0)

sphere = Sphere(np.array([0, 1.0, 0]), 1.0, sphere_material)
plane = Plane(np.array([0.0, 0.0, 0.0]), np.array([0.0, 1.0, 0.0]), plane_material)

scene.add_shape(plane)
scene.add_shape(sphere)

light_material = Material(Color(1, 1, 1), Color(1, 1, 1), Color(1, 1, 1), 100.0)
light = PointLight(np.array([-3.0, 5.0, 1.0]), light_material)

scene.add_light_source(light)

image = Image(1920, 1080)
camera = Camera(np.array([-5.0, 1.0, 0.0]), np.array([0.0, 1.0, 0.0]), 
                np.array([0.0, 1.0, 0.0]), 25 * math.pi / 180.0, image.width / image.height)

ray_trace(image, scene, camera)
image.save("output.jpg")
image.save("gamma_corrected.jpg", True)