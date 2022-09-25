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

    # Check if this position is in the board (use Board.size as argument)
    def InBoard(self, size:tuple[int,int]):
        return self.x >= 0 and self.y >= 0 and self.x < size[0] and self.y < size[1]

    # DO NOT MOVE but return a preview of the coordinates
    def __add__(self, movement:Vector):
        return Position(self.x + movement.x, self.y + movement.y)
    
    # Vector from other position to self
    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return Vector(self.x - other.x, self.y - other.y)
        else:
            raise TypeError(f'{type(other)} is not a Position')