# Représente un vecteur. Utilisé tel quel il s'agira souvent d'un mouvement
class Vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Utilisée pour représenter une position (vecteur depuis l'origine)
class Position(Vector):
    def convert(self):
        print("Position.convert() NYI")
    def Move(self, movement:Vector):
        self.x += movement.x
        self.y += movement.y