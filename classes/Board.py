from classes.Position import Position

# Class for a board
class Board():
    def __init__(self, size:tuple[int,int]):
        # size[0] is the width and size[1] is height
        self.size = size
        # Contain all the elelments
        self.all = [[None for i in range(self.size[0])] for j in range(self.size[1])]

    # Set a new object on the board
    def NewObject(self, coordinates:Position, newObject):
        self.all[coordinates.y][coordinates.x] = newObject

    # Move selected object
    def MoveObject(self, oldCoordinates:Position, newCoordinates:Position):
        movedObject = self.all[oldCoordinates.y][oldCoordinates.x]
        self.all[oldCoordinates.y][oldCoordinates.x] = None
        self.all[newCoordinates.y][newCoordinates.x] = movedObject

    # Delete the object at targeted position
    def DeleteObject(self, coordinates:Position):
        self.all[coordinates.y][coordinates.x] = None

    # Checking has to be down before movement for preventing unwanted deletion
    def IsCaseOccupied(self, coordinates:Position):
        return self.all[coordinates.y][coordinates.x] != None
    
    # Return the object in targeted position
    def SelectPosition(self,coordinates:Position):
        return self.all[coordinates.y][coordinates.x]