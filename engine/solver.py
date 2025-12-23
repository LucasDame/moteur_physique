from engine.vector2D import Vector2D as Vector
from engine.bodies.body import Body
from engine.bodies.wall import Wall
from engine.bodies.ball import Ball
from engine.bodies.polygon import Polygon
import math

class Solver:

    def __init__(self):
        pass

    def solve(self, world, dt: float):
        bodies = world.bodies
        n = len(bodies)
        for i in range(n):
            for j in range(i + 1, n):
                bodyA = bodies[i]
                bodyB = bodies[j]

                # Vérifier la collision entre bodyA et bodyB
                if isinstance(bodyA, Wall) and isinstance(bodyB, Ball):
                    self.solve_wall_ball_collision(bodyA, bodyB)
                elif isinstance(bodyA, Ball) and isinstance(bodyB, Wall):
                    self.solve_wall_ball_collision(bodyB, bodyA)
                elif isinstance(bodyA, Ball) and isinstance(bodyB, Ball):
                    self.solve_ball_collision(bodyA, bodyB)
                elif isinstance(bodyA, Polygon) and isinstance(bodyB, Ball):
                    self.solve_polygon_ball_collision(bodyA, bodyB)
                elif isinstance(bodyA, Ball) and isinstance(bodyB, Polygon):
                    self.solve_polygon_ball_collision(bodyB, bodyA)
    
    def solve_wall_ball_collision(self, wall: Wall, ball: Ball):

        # 1. Vecteur distance
        delta = ball.pos - wall.pos

        # 2. Gestion de l'angle
        # D'après ton renderer, wall.angle est déjà en radians !
        angle_rad = wall.angle 
        
        # Pour passer du Monde au Local, on tourne à l'envers (-angle)
        cos_a = math.cos(-angle_rad)
        sin_a = math.sin(-angle_rad)

        # 3. Projection en Local (Rotation)
        local_x = delta.x * cos_a - delta.y * sin_a
        local_y = delta.x * sin_a + delta.y * cos_a

        # 4. Clamping (ADAPTÉ AU RENDERER)
        # Ton renderer met la "Length" sur X et la "Width" sur Y
        half_len_x = wall.length / 2  
        half_wid_y = wall.width / 2   

        # On clamp X par rapport à la Length
        closest_x = max(-half_len_x, min(local_x, half_len_x))
        # On clamp Y par rapport à la Width
        closest_y = max(-half_wid_y, min(local_y, half_wid_y))

        # 5. Vérification de la distance
        dist_x = local_x - closest_x
        dist_y = local_y - closest_y
        dist_sq = dist_x**2 + dist_y**2
        
        if dist_sq > ball.radius ** 2:
            return # Pas de collision

        # 6. Résolution
        distance = math.sqrt(dist_sq)

        # Normale en espace Local
        if distance == 0:
            local_normal = Vector(0, -1)
            penetration = ball.radius
        else:
            local_normal = Vector(dist_x / distance, dist_y / distance)
            penetration = ball.radius - distance
            
        # 7. Retour en espace Monde (Rotation normale +angle)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        
        world_normal_x = local_normal.x * cos_a - local_normal.y * sin_a
        world_normal_y = local_normal.x * sin_a + local_normal.y * cos_a
        world_normal = Vector(world_normal_x, world_normal_y)
        
        # A. Correction de Position (Repousse la balle hors du mur)
        ball.pos += world_normal * penetration
        
        # B. Réponse Physique (Rebond)
        restitution = ball.restitution if ball.restitution < wall.restitution else wall.restitution
        
        # Produit scalaire pour savoir si la balle va vers le mur
        vel_along_normal = ball.vel.dot(world_normal)
        
        if vel_along_normal < 0:
            j = -(1 + restitution) * vel_along_normal
            impulse = world_normal * j
            ball.vel += impulse
    
    def solve_ball_collision(self, b1: Body, b2: Body):

        delta = b2.pos - b1.pos

        dist = delta.norm()
        radius_sum = b1.radius + b2.radius

        if dist >= radius_sum:
            return  # Pas de collision

        else:
            if dist != 0:
                
                penetration = radius_sum - dist
                delta_normalized = delta.normalized()

                total_inv_mass = b1.inv_mass + b2.inv_mass
                
                if total_inv_mass == 0: return # Deux objets infinis immobiles

                move_per_inv_mass = delta_normalized * (penetration / total_inv_mass)
                b1.pos -= move_per_inv_mass * b1.inv_mass
                b2.pos += move_per_inv_mass * b2.inv_mass
        
        restitution = min(b1.restitution, b2.restitution)

        rel_vel = b2.vel - b1.vel
        vel_along_normal = rel_vel.dot(delta_normalized)

        if vel_along_normal > 0:
            return  # Les corps s'éloignent

        j = -(1 + restitution) * vel_along_normal
        j /= total_inv_mass

        impulse = delta_normalized * j
        b1.vel -= impulse * b1.inv_mass
        b2.vel += impulse * b2.inv_mass

    def solve_polygon_ball_collision(self, poly: Polygon, ball: Ball):
        vertices = poly.get_vertices()
        
        # Initialisation des variables pour trouver le point d'impact
        best_dist_sq = float('inf')
        best_closest_point = None
        
        # On parcourt chaque segment du polygone
        for i in range(len(vertices)):
            
            # --- 1. TRANSFORMATION LOCAL -> MONDE ---
            
            # Version avec Rotation (si ton moteur le supporte)
            v1_local = vertices[i]
            v2_local = vertices[(i + 1) % len(vertices)]
            
            # Sinon (simple translation) :
            va = poly.pos + v1_local
            vb = poly.pos + v2_local

            # --- 2. PROJECTION SUR LE SEGMENT ---
            edge = vb - va
            to_ball = ball.pos - va
            
            edge_len_sq = edge.mag_sq() # Utilise le carré pour la perf (si dispo)
            if edge_len_sq == 0: continue # Évite la division par zéro

            # Projection t (entre 0 et 1)
            t = to_ball.dot(edge) / edge_len_sq
            t = max(0, min(1, t))

            # Point le plus proche sur ce segment (en Monde)
            closest = va + edge * t
            
            # Distance au carré (plus rapide que la racine carrée)
            dist_vec = ball.pos - closest
            dist_sq = dist_vec.mag_sq()

            # On garde le point le plus proche de tout le tour du polygone
            if dist_sq < best_dist_sq:
                best_dist_sq = dist_sq
                best_closest_point = closest

        # --- 3. VÉRIFICATION COLLISION ---
        # Si la distance la plus courte est supérieure au rayon, on ne touche pas
        if best_dist_sq >= ball.radius ** 2:
            return 

        # --- 4. RÉSOLUTION ---
        distance = math.sqrt(best_dist_sq)
        
        # Calcul de la normale
        if distance == 0:
            normal = Vector(0, -1)
        else:
            # Normale : Du mur VERS la balle
            normal = (ball.pos - best_closest_point) / distance
        
        # Important : La normale est toujours "Balle - Mur".
        # Que le polygone soit vide ou plein, on veut repousser la balle Loin du mur.
        # Donc la logique reste la même.

        penetration = ball.radius - distance

        # Physique (Masse infinie etc.)
        total_inv_mass = poly.inv_mass + ball.inv_mass
        if total_inv_mass == 0: return 

        move_per_inv_mass = normal * (penetration / total_inv_mass)
        
        # On bouge les objets pour qu'ils ne se chevauchent plus
        poly.pos -= move_per_inv_mass * poly.inv_mass
        ball.pos += move_per_inv_mass * ball.inv_mass

        # Calcul de l'impulsion (Rebond)
        restitution = min(poly.restitution, ball.restitution)
        rel_vel = ball.vel - poly.vel
        vel_along_normal = rel_vel.dot(normal)

        # Si ça s'éloigne déjà, on ne fait rien
        if vel_along_normal > 0:
            return 

        j = -(1 + restitution) * vel_along_normal
        j /= total_inv_mass

        impulse = normal * j
        poly.vel -= impulse * poly.inv_mass
        ball.vel += impulse * ball.inv_mass