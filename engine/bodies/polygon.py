from engine.bodies.body import Body
from engine.vector2D import Vector2D as Vector

class Polygon(Body):
    def __init__(self, position: "Vector" = Vector(0, 0),
                    velocity: "Vector" = Vector(0, 0),
                    acceleration: "Vector" = Vector(0, 0),
                    vertices: list["Vector"] = [],
                    mass: float = 0,
                    type : bool = True,
                    restitution : float = 1.0):

        super().__init__(position, velocity, acceleration, mass, restitution=restitution)
        self.vertices = vertices  # Liste de sommets définissant le polygone
        self.type = type  # Type du polygone (True pour un polygone plein, False pour un polygone extrudé)

    def get_vertices(self) -> list["Vector"]:
        return self.vertices
    
    def set_vertices(self, vertices: list["Vector"]):
        self.vertices = vertices

    def update(self, dt: float):
        super().update(dt)
    
    def get_type(self) -> bool:
        return self.type
    
    def set_type(self, type: bool):
        self.type = type
    
    def compute_inertia(self):
        return super().compute_inertia()