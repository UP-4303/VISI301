from classes.Position import Position as Position

# Class for a board
class Board():
    def __init__(self, size:tuple[int,int]):
        # size[0] is the width and size[1] is height
        self.size = size
        # Contain all the elelments
        self.all = [[None for i in range(self.size[0])] for j in range(self.size[1])]

    # Set a new object on the board
    def NewObject(self, coordinates:Position, newObject):
        self.all[coordinates.x][coordinates.y] = newObject

    # Move selected object
    def MoveObject(self, oldCoordinates:Position, newCoordinates:Position):
        movedObject = self.all[oldCoordinates.x][oldCoordinates.y]
        self.all[oldCoordinates.x][oldCoordinates.y] = None
        self.all[newCoordinates.x][newCoordinates.y] = movedObject

    def DeleteObject(self, coordinates:Position):
        self.all[coordinates.x][coordinates.y] = None

    # Checking has to be down before movement for preventing unwanted deletion
    def IsCaseOccupied(self, coordinates:Position):
        return self.all[coordinates.x][coordinates.y] != None