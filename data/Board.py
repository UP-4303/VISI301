class Board():
    def __init__(self, size:tuple[int,int]):
        # size[0] is the width and size[1] is height
        self.size = size
        self.all = [['' for i in range(self.size[0])] for j in range(self.size[1])]

    def Update(self, coordinates:tuple[int,int], newObject):
        self.all[coordinates[0]][coordinates[1]] = newObject
        return self

    def IsCaseOccupied(self, coordinates:tuple[int,int]):
        return self.all[coordinates[0]][coordinates[1]] != ''