from ray import Ray

class Intersection:
    def __init__(self, ray: Ray, shape = None, t: float = None, color = None):
        self.ray = ray
        self.t = t
        if t is None:
            self.t = ray.max_t
        self.intersected_shape = None
        self.color = color

    def intersected(self):
        return self.intersected_shape != None

    def position(self):
        return self.ray.ray_point(self.t)

    def __lt__(self, other):
        if not isinstance(other, Intersection):
            raise TypeError("Can compare only with Intersection")

        return self.t < other.t