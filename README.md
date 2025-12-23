# 🍎 Moteur Physique 2D (Python & Tkinter)

Un moteur physique construit "from scratch" en Python pour comprendre les mathématiques derrière la simulation de mouvement, la gravité et les collisions. 

Ce projet utilise **Tkinter** pour le rendu graphique, mais l'architecture sépare strictement la logique physique (`engine`) de l'interface graphique (`gui`), permettant une grande flexibilité.

## 🚀 Fonctionnalités Actuelles

* **Architecture découplée** : Séparation nette entre le modèle (Physique) et la vue (Tkinter).
* **Mathématiques vectorielles** : Librairie `Vector2D` faite maison (pas de NumPy).
* **Physique réaliste** :
    * Intégration d'Euler Semi-Implicite pour le mouvement.
    * Gestion de la gravité ($9.81 m/s^2$).
    * Système de masse et d'accélération ($F = m \times a$).
* **Système de Rendu** :
    * Gestion de l'échelle **PPM** (Pixels Per Meter) pour convertir les mètres (physique) en pixels (écran).
    * Boucle de rendu fluide à 60 FPS.

## 📂 Architecture du Projet

```text
MOTEUR_PHYSIQUE/
│
├── engine/                 # LE CŒUR (Logique Pure)
│   ├── bodies/             # Les objets physiques
│   │   ├── body.py         # Classe abstraite parente
│   │   └── ball.py         # Implémentation d'une balle (Cercle)
│   ├── vector2D.py         # Classe utilitaire pour les vecteurs (x, y)
│   └── world.py            # Le "Monde" : gère la gravité et la liste des objets
│
├── gui/                    # L'INTERFACE (Rendu)
│   ├── renderer.py         # Traduit les objets physiques en dessins Tkinter
│   └── (window.py)         # (À venir : gestion fenêtre)
│
├── main.py                 # POINT D'ENTRÉE : Lance la boucle et la scène
└── README.md
```

## 🛠️ Installation et Exécution

1. **Prérequis** :
   - Python 3.10 ou supérieur
   - Tkinter (inclus par défaut dans Python)

2. **Exécution** :
   ```bash
   python main.py
   ```

## 📈 Prochaines Étapes

[x] Moteur de base (Vecteurs, Gravité, Boucle de jeu)

[x] Système de rendu séparé

[x] Conversion Mètres <-> Pixels (PPM)

[ ] Collisions : Détection Balle-Mur (Rebond simple)

[ ] Collisions : Détection Balle-Balle

[ ] Nouvelle forme : Rectangles / Boîtes

[ ] Souris : Attraper et lancer les objets

[ ] Interface Utilisateur : Contrôles de la simulation (Pause, Vitesse, Ajout d'objets)

[ ] Optimisations : Améliorer les performances pour plus d'objets

