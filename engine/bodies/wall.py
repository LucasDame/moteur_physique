from engine.bodies.body import Body
from engine.vector2D import Vector2D as Vector
import math

class Wall(Body):

    def __init__(self, position = Vector(0, 0), velocity = Vector(0, 0), acceleration = Vector(0, 0), width = 1.0, length = 1.0, angle = 0.0, color=None, mass=0.0, restitution = 1.0):
        super().__init__(position, velocity, acceleration, mass, color, restitution)
        self.width = width
        self.length = length
        self.angle = math.radians(angle)

    def get_width(self) -> float:
        return self.width
    
    def set_width(self, width):
        self.width = width

    def get_length(self) -> float:
        return self.length

    def set_length(self, length):
        self.length = length
    
    def get_angle(self) -> float:
        return self.angle
    
    def set_angle(self, angle):
        self.angle = angle

    def get_normal(self) -> "Vector":
        # Retourne la normale du mur (vecteur perpendiculaire)
        rad = (self.angle)
        normal_x = -math.sin(rad)
        normal_y = math.cos(rad)
        return Vector(normal_x, normal_y)

    def get_tangent(self) -> "Vector":
        # Retourne la direction du mur (vecteur tangent)
        rad = (self.angle)
        dir_x = math.cos(rad)
        dir_y = math.sin(rad)
        return Vector(dir_x, dir_y)
    
    def compute_inertia(self):
        return float('inf')  # Mur immobile