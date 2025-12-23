from abc import ABC, abstractmethod
from engine.vector2D import Vector2D as Vector

class Body(ABC):
    def __init__(self, position = Vector(0, 0), velocity = Vector(0, 0), acceleration = Vector(0, 0), mass = 1.0, color=None, restitution = 1.0):
        self.pos = position
        self.vel = velocity
        self.acc = acceleration

        self.mass = mass
        self.restitution = restitution
        self.inv_mass = 1 / mass if mass > 0 else 0 

        self.forces = Vector(0, 0)

        self.color = color if color else "black"

    def get_position(self) -> "Vector" :
        return self.pos

    def set_position(self, x, y) :
        self.pos = Vector(x, y)

    def get_velocity(self) -> "Vector" :
        return self.vel

    def set_velocity(self, vx, vy) :
        self.vel = Vector(vx, vy)

    def get_acceleration(self) -> "Vector" :
        return self.acc

    def set_acceleration(self, ax, ay) :
        self.acc = Vector(ax, ay)

    def get_mass(self) -> float :
        return self.mass
    
    def set_mass(self, mass) :
        self.mass = mass
    
    def get_color(self) -> str :
        return self.color
    
    def set_color(self, color) :
        self.color = color

    def apply_force(self, force):
        self.forces += force
    
    def is_static(self) -> bool:
        return (self.mass == 0)or (self.vel.norm() == 0 and self.forces.norm() == 0)

    def update(self, dt):
        if self.mass == 0: return  # Objet statique, ne bouge pas

        self.acc = self.forces * self.inv_mass

        self.vel += self.acc * dt

        self.pos += self.vel * dt

        self.forces = Vector(0, 0)

    @abstractmethod
    def compute_inertia(self):
        """Chaque forme devra définir comment elle calcule son inertie"""
        pass