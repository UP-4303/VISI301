from classes.Vector import Vector as Vector

# Utilisée pour représenter une position (vecteur depuis l'origine)
class Position(Vector):
    def convert(self):
        print("Position.convert() NYI")
        
    def Move(self, movement:Vector):
        self.x += movement.x
        self.y += movement.y