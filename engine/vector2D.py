class Vector2D :

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __add__(self, other) -> 'Vector2D':
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other) -> 'Vector2D':
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar) -> 'Vector2D':
        return Vector2D(self.x * scalar, self.y * scalar)
    
    def __truediv__(self, scalar) -> 'Vector2D':
        return Vector2D(self.x / scalar, self.y / scalar)
    
    def dot(self, other) -> float:
        return self.x * other.x + self.y * other.y
    
    def norm(self) -> float:
        return (self.x**2 + self.y**2) ** 0.5
    
    def normalized(self) -> 'Vector2D':
        n = self.norm()
        if n == 0:
            return Vector2D(0, 0)
        return self / n
    
    def mag_sq(self) -> float:
        return self.x**2 + self.y**2