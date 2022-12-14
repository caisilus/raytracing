from ray import Ray

class Intersection:
    def __init__(self, ray: Ray, shape = None, t: float = None):
        self.ray = ray
        self.t = t
        if t is None:
            self.t = ray.max_t
        self.intersected_shape = shape

    def material(self):
        return self.intersected_shape.material

    def normal(self):
        return self.intersected_shape.normal_at_point(self.position())

    def intersected(self):
        return self.intersected_shape != None

    def position(self):
        return self.ray.ray_point(self.t)

    def __lt__(self, other):
        if not isinstance(other, Intersection):
            raise TypeError("Can compare only with Intersection")

        return self.t < other.t