import tkinter as tk
import math
from engine.bodies.ball import Ball
from engine.bodies.wall import Wall
from engine.bodies.polygon import Polygon

class Renderer:
    def __init__(self, canvas: tk.Canvas, ppm : float):
        self.canvas = canvas
        self.ppm = ppm
        self.colors = {
            "ball": "#FF5733",
            "wall": "#333333",
            "polygon": "#33FF57"
        }

    def clear(self):
        self.canvas.delete("all")

    def draw_world(self, world):
        self.clear()

        for body in world.bodies:
            if isinstance(body, Ball):
                self.draw_ball(body)
            elif isinstance(body, Wall):
                self.draw_wall(body)
            elif isinstance(body, Polygon):
                self.draw_polygon(body)
            else:
                print(f"Type d'objet inconnu : {type(body)}")

    # --- Méthodes de dessin spécifiques ---

    def draw_ball(self, ball):
        # 1. On convertit la position (x, y) en pixels
        screen_x = ball.pos.x * self.ppm
        screen_y = ball.pos.y * self.ppm
        
        # 2. On convertit le rayon en pixels
        screen_radius = ball.radius * self.ppm
        
        # --- DESSIN (Bounding Box Tkinter) ---
        x0 = screen_x - screen_radius
        y0 = screen_y - screen_radius
        x1 = screen_x + screen_radius
        y1 = screen_y + screen_radius
        
        self.canvas.create_oval(x0, y0, x1, y1, fill=self.colors["ball"])
    
    def draw_wall(self, wall):

        half_w = (wall.width / 2) * self.ppm
        half_l = (wall.length / 2) * self.ppm
        
        cx = wall.pos.x * self.ppm
        cy = wall.pos.y * self.ppm

        angle_rad = (wall.angle)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)

        corners = [
            (-half_l, -half_w),
            ( half_l, -half_w),
            ( half_l,  half_w),
            (-half_l,  half_w)
        ]

        for i in range(len(corners)):
            x_old, y_old = corners[i]
            x_new = cx + (x_old * cos_a - y_old * sin_a)
            y_new = cy + (x_old * sin_a + y_old * cos_a)
            corners[i] = (x_new, y_new)
        
        self.canvas.create_polygon(corners, fill=self.colors["wall"])
    
    def draw_polygon(self, polygon: Polygon):
        # 1. Calcul des points du polygone (Conversion Monde -> Écran)
        poly_points = []
        for vertex in polygon.get_vertices():
            screen_x = (polygon.pos.x + vertex.x) * self.ppm
            screen_y = (polygon.pos.y + vertex.y) * self.ppm
            poly_points.append(screen_x)
            poly_points.append(screen_y)

        if polygon.get_type():
            # --- CAS 1 : Polygone Plein (Normal) ---
            # On dessine juste la forme remplie
            self.canvas.create_polygon(
                poly_points, 
                fill=self.colors["polygon"], 
                outline="black", 
                width=2
            )
        else:
            # --- CAS 2 : Polygone "Extrudé" (Mur avec un trou) ---
            # On veut dessiner tout l'écran EN GRIS, sauf l'intérieur du polygone.
            
            # RÉCUPÉRATION DYNAMIQUE DE LA TAILLE
            # C'est ça qui garantit que le mur couvre tout l'écran, quelle que soit la résolution
            w = self.canvas.winfo_width()
            h = self.canvas.winfo_height()
            
            # On prend une marge énorme (10 fois la hauteur actuelle)
            huge = h * 10
            
            # Les 4 coins du "Monde" (Sens Horaire)
            world_border = [
                -huge, -huge,  # Haut-Gauche
                 huge, -huge,  # Haut-Droite
                 huge,  huge,  # Bas-Droite
                -huge,  huge,  # Bas-Gauche
                -huge, -huge   # Retour au Haut-Gauche
            ]

            if len(poly_points) >= 2:
                inner_shape = poly_points + [poly_points[0], poly_points[1]]
            else:
                inner_shape = poly_points
            
            # B. Fusion des formes
            # On dessine une forme unique qui contient le bord du monde ET le polygone.
            # Tkinter va "soustraire" le polygone du rectangle géant.
            total_shape = world_border + inner_shape
            
            # C. Dessin
            # Note : On utilise la couleur "wall" car c'est de la matière "mur"
            self.canvas.create_polygon(
                total_shape, 
                fill=self.colors["wall"], # Remplissage gris (Mur)
                width=2
            )