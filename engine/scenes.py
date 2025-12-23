from engine.vector2D import Vector2D as Vector
from engine.bodies.polygon import Polygon
from engine.bodies.ball import Ball
from engine.bodies.wall import Wall
from engine.world import World

import random

def floor_scene(world : World,canvas_width : int, canvas_height : int, ppm : float):
    floor = Wall(
        position=Vector(canvas_width / (2 * ppm), canvas_height / ppm),
        width=1,
        length=canvas_width / ppm,
        angle=0,
        mass=0
    )
    world.add_body(floor)
    
def cage_scene(world : World,canvas_width : int, canvas_height : int, ppm : float):
    floor = Wall(
        position=Vector(canvas_width / (2 * ppm), canvas_height / ppm),
        width=1,
        length=canvas_width / ppm,
        angle=0,
        mass=0
    )
    left_wall = Wall(
        position=Vector(0, canvas_height / (2 * ppm)),
        width=1,
        length=canvas_height / ppm,
        angle=90,
        mass=0
    )
    right_wall = Wall(
        position=Vector(canvas_width / ppm, canvas_height / (2 * ppm)),
        width=1,
        length=canvas_height / ppm,
        angle=90,
        mass=0
    )
    ceiling = Wall(
        position=Vector(canvas_width / (2 * ppm), 0),
        width=1,
        length=canvas_width / ppm,
        angle=0,
        mass=0
    )
    world.add_body(floor)
    world.add_body(left_wall)
    world.add_body(right_wall)
    world.add_body(ceiling)

def balls_scene(world : World, num_balls : int, canvas_width : int, canvas_height : int, ppm : float):
    for _ in range(num_balls):
        ball = Ball(
            position=Vector(random.uniform(1, canvas_width / ppm), random.uniform(1, canvas_height / ppm)),
            radius=random.uniform(0.2, 0.5),
            mass=random.uniform(1, 5)
        )
        world.add_body(ball)

def polygon_scene(world : World, num_polygons : int, canvas_width : int, canvas_height : int, ppm : float):
    for _ in range(num_polygons):
        size = random.uniform(0.5, 1.5)
        polygon = Polygon(
            position=Vector(random.uniform(1, canvas_width / ppm), random.uniform(1, canvas_height / ppm)),
            vertices=[
                Vector(-size, -size),
                Vector(size, -size),
                Vector(size, size),
                Vector(-size, size)
            ],
            mass=0,
            type=True
        )
        world.add_body(polygon)
    
def poly_cage_scene(world : World, canvas_width : int, canvas_height : int, ppm : float):
    thickness = 1
    cage_height = (canvas_height) / ppm - thickness
    cage_width = (canvas_width) / ppm - thickness
    cage = Polygon(
        position=Vector(canvas_width / (2 * ppm), canvas_height / (2 * ppm)),
        vertices=[
            Vector(-cage_width / 2, -cage_height / 2),
            Vector(cage_width / 2, -cage_height / 2),
            Vector(cage_width / 2, cage_height / 2),
            Vector(-cage_width / 2, cage_height / 2)
        ],
        mass=0,
        type=False
    )
    world.add_body(cage)


def bouncing_scene(world : World):
    ball1 = Ball(
        position=Vector(4, 3), 
        velocity=Vector(10, 0), 
        radius=0.4,            
        mass=5                 
    )
    
    ball2 = Ball(
        position=Vector(6, 2), 
        velocity=Vector(-10, 0),
        radius=0.2,            
        mass=10
    )

    wall1 = Wall(
        position=Vector(5, 8),
        width=1,
        length=20,
        angle = 20,
        mass=0
    )

    wall2 = Wall(
        position=Vector(1, 4),
        width=1,
        length=12,
        angle = 85,
        mass=0
    )

    wall4 = Wall(
        position=Vector(10, 4),
        width=1,
        length=12,
        angle = -85,
        mass=0
    )

    wall3 = Wall(
        position=Vector(5, 1),
        width=1,
        length=20,
        angle = 0,
        mass=0
    )

    world.add_body(ball1)
    world.add_body(ball2)
    world.add_body(wall1)
    world.add_body(wall2)
    world.add_body(wall3)
    world.add_body(wall4)

def every_collision_scene(world : World):
    ball = Ball(
        position=Vector(5, 5), 
        velocity=Vector(2, 0), 
        radius=0.5,            
        mass=5                 
    )

    wall = Wall(
        position=Vector(5, 8),
        width=1,
        length=20,
        angle = 0,
        mass=0
    )

    polygon = Polygon(
        position=Vector(7, 5),
        vertices=[
            Vector(-1, -1),
            Vector(1, -1),
            Vector(1, 1),
            Vector(-1, 1)
        ],
        mass=0,
        type=True
    )

    world.add_body(ball)
    world.add_body(wall)
    world.add_body(polygon)