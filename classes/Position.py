from classes.Vector import Vector

# A vector (from the origin) with some usefull methods
class Position(Vector):
    # When graphical interface will be implemented, it will convert in-game position to pygame's window coordinates and vice-versa
    def convert(self):
        print("Position.convert() NYI")
    
    # Move the coordinates
    def Move(self, movement:Vector):
        self.x += movement.x
        self.y += movement.y
    
    # DO NOT MOVE but return a preview of the coordinates
    def __add__(self, movement:Vector):
        return Position(self.x + movement.x, self.y + movement.y)
    
    # Vector from position to self
    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return Vector(self.x - other.x, self.y - other.y)
        else:
            raise TypeError(f'{type(other)} is not a Position')