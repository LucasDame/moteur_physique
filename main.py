import tkinter as tk
import time
import math

from gui.renderer import Renderer
from engine.world import World

from engine.vector2D import Vector2D as Vector
from engine.bodies.ball import Ball
from engine.bodies.wall import Wall
from engine.bodies.polygon import Polygon
import engine.scenes as scenes

# Simulation settings

FPS = 60
DT = 1 / FPS  # Delta time (temps écoulé entre deux images)

PPM = 30.0  # Pixels Per Meter

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Moteur Physique Python")

        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", lambda event: self.root.destroy())

        self.canvas = tk.Canvas(self.root, bg="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()

        self.renderer = Renderer(self.canvas, PPM)
        self.world = World()

        self.setup_scene()

        self.time_start = time.time()
        self.update()

    def setup_scene(self):
        scenes.poly_cage_scene(self.world, self.width, self.height, PPM)
        scenes.balls_scene(self.world, 50, self.width, self.height, PPM)
        scenes.polygon_scene(self.world, 3, self.width, self.height, PPM)

    def update(self):
        buffer = self.time_start
        self.time_start = time.time()
        dt = self.time_start - buffer
        real_fps = 1 / dt if dt > 0 else FPS

        self.world.step(DT)
        
        self.renderer.draw_world(self.world)
        self.canvas.create_text(10, 10, text="fps: {:.2f}".format(real_fps), anchor="nw", fill="grey", font=("Arial", 16))

        time_end = time.time()
        elapsed = time_end - self.time_start
        self.root.after(int(1000/FPS - elapsed * 1000), self.update)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()