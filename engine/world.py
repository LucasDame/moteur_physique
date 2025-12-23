from engine.vector2D import Vector2D as Vector
from engine.bodies.body import Body
from engine.solver import Solver

class World:

    def __init__(self, gravity = Vector(0, 9.81), friction_coefficient: float = 0.1):
        self.bodies = []
        self.gravity = gravity
        self.friction_coefficient = friction_coefficient
        self.solver = Solver()

    def get_gravity(self) -> "Vector":
        return self.gravity
    
    def set_gravity(self, gravity: "Vector"):
        self.gravity = gravity

    def add_body(self, body: "Body"):
        self.bodies.append(body)
    
    def get_bodies(self) -> list:
        return self.bodies
    
    def remove_body(self, body: "Body"):
        if body in self.bodies:
            self.bodies.remove(body)

    def step(self, dt):
        for body in self.bodies:
            # Appliquer la gravité
            if body.get_mass() > 0:  # Ne pas appliquer la gravité aux
                body.apply_force(self.gravity * body.get_mass())

            # Appliquer la friction
            if body.get_velocity().norm() > 1:
                friction_force = body.get_velocity().normalized() * (body.get_velocity().norm()**2) * - self.friction_coefficient
            else:
                friction_force = body.get_velocity() * - self.friction_coefficient
            body.apply_force(friction_force)

            body.update(dt)

        self.solver.solve(self, dt)
    
