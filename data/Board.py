from data.Vector import Position as Position

class Board():
    def __init__(self, size:tuple[int,int]):
        # size[0] is the width and size[1] is height
        self.size = size
        self.all = [['' for i in range(self.size[0])] for j in range(self.size[1])]

    def Update(self, coordinates:Position, newObject):
        self.all[coordinates.x][coordinates.y] = newObject

    def IsCaseOccupied(self, coordinates:Position):
        return self.all[coordinates.x][coordinates.y] != ''