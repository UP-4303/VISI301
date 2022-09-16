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
    def MovePreview(self, movement:Vector):
        return Position(self.x + movement.x, self.y + movement.y)