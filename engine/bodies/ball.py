from engine.bodies.body import Body
from engine.vector2D import Vector2D as Vector

class Ball(Body):

    def __init__(self, position = Vector(0, 0), velocity = Vector(0, 0), acceleration = Vector(0, 0), radius = 10, color=None, mass=1.0, restitution=1.0):
        super().__init__(position, velocity, acceleration, mass, color, restitution)
        self.radius = radius

    def compute_inertia(self):
        return 0.5 * self.mass * (self.radius ** 2)

    def get_radius(self) -> float:
        return self.radius
    
    def set_radius(self, radius):
        self.radius = radius