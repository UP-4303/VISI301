from classes.Position import Position

class PathNode():
    def __init__(self, coordinates:Position, gCost, hCost):
        self.coordinates = coordinates
        self.gCost = gCost
        self.hCost = hCost
    
    def Update(self, gCost, hCost):
        self.gCost = gCost
        self.hCost = hCost
    
    def Cost(self):
        return self.gCost + self.hCost