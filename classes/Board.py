from classes.Position import Position as Position

# Classe de plateau, dont la variable la plus un importante, (Board.all) est un tableau de tableau contenant tout les éléments
class Board():
    def __init__(self, size:tuple[int,int]):
        # size[0] is the width and size[1] is height
        self.size = size
        self.all = [[None for i in range(self.size[0])] for j in range(self.size[1])]

    def NewObject(self, coordinates:Position, newObject):
        self.all[coordinates.x][coordinates.y] = newObject

    def Move(self, oldCoordinates:Position, newCoordinates:Position):
        movedObject = self.all[oldCoordinates.x][oldCoordinates.y]
        self.all[oldCoordinates.x][oldCoordinates.y] = None
        self.all[newCoordinates.x][newCoordinates.y] = movedObject

    def IsCaseOccupied(self, coordinates:Position):
        return self.all[coordinates.x][coordinates.y] != None