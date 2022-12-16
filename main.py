from camera import Camera
from scene import Scene
from sphere import Sphere
from plane import Plane
from box import Box
from image import Image
from color import Color
from material import Material
from point_light import PointLight

import numpy as np
import math
import time

from raytrace import ray_trace

def build_scene():
    scene = Scene()

    walls_shineness = 0.0

    walls_specular_color = Color.gray(0.0)

    floor_material = Material(Color.gray(0.1), Color.gray(0.5), walls_specular_color, walls_shineness)
    floor = Plane(np.array([0.0, 0.0, 0.0]), np.array([0.0, 1.0, 0.0]), floor_material)

    right_wall_material = Material(Color.blue(0.1), Color.blue(0.7), walls_specular_color, walls_shineness)
    right_wall = Plane(np.array([5.0, 0.0, 0.0]), np.array([-1.0, 0.0, 0.0]), right_wall_material)

    left_wall_material = Material(Color.red(0.1), Color.red(0.7), walls_specular_color, walls_shineness)
    left_wall = Plane(np.array([-5.0, 0.0, 0.0]), np.array([1.0, 0.0, 0.0]), left_wall_material)

    back_wall_material = Material(Color.green(0.1), Color.green(0.5), walls_specular_color, walls_shineness, 0.8)
    back_wall = Plane(np.array([0.0, 0.0, 10.0]), np.array([0.0, 0.0, -1.0]), back_wall_material)
    roof = Plane(np.array([0.0, 10.0, 0.0]), np.array([0.0, -1.0, 0.0]), floor_material)

    front_wall = Plane(np.array([0.0, 0.0, -11.0]), np.array([0.0, 0.0, 1.0]), floor_material)

    scene.add_shape(floor)
    scene.add_shape(left_wall)
    scene.add_shape(right_wall)
    scene.add_shape(back_wall)
    scene.add_shape(front_wall)
    scene.add_shape(roof)

    box_material = Material(Color.turquoise(0.1), Color.turquoise(0.9), Color.gray(0.0), 0.0, 0.0)
    box = Box(np.array([2.5, 2.0, 6.0]), 3.0, 4.0, 3.0, box_material)
    sphere_material = Material(Color.yellow(0.1), Color.yellow(0.7), Color.gray(1.0))
    sphere = Sphere(np.array([1.0, 1.0, 3.0]), 1.0, sphere_material)
    reflecting_material = Material(Color.purple(0.1), Color.purple(0.7), Color.gray(0.0), 0.0, 0.6)
    reflecting_sphere = Sphere(np.array([-2.0, 2.0, 6.0]), 2.0, reflecting_material)
    
    scene.add_shape(box)
    scene.add_shape(sphere)
    scene.add_shape(reflecting_sphere)

    light_material = Material(Color(1, 1, 1), Color(1, 1, 1), Color(1, 1, 1), 100.0)
    light = PointLight(np.array([0.0, 9.0, 6.0]), light_material)

    scene.add_light_source(light)

    return scene


def main():
    scene = build_scene()
    #image = Image(1920, 1080)
    # image = Image(1280, 720)
    image = Image(640, 360)
    camera = Camera(np.array([0.0, 5.0, -10.0]), np.array([0.0, 5.0, 2.0]), 
                    np.array([0.0, 1.0, 0.0]), 25 * math.pi / 180.0, image.width / image.height)

    tic = time.perf_counter()
    ray_trace(image, scene, camera)
    tac = time.perf_counter()
    print(f"Rendering time: {(tac - tic) / 60.0}")
    image.save("output.jpg")

    # print("saved output")
    # image.save("gamma_corrected.jpg", True, 1.4, 2.2)
    # print("saved gamma_corrected")

if __name__ == "__main__":
    main()