from math import nan

from classes.Position import Position

class PathNode():
    def __init__(self, explored:bool=False, gCost:int=nan, hCost:int=nan):
        self.explored = explored
        self.gCost = gCost
        self.hCost = hCost

    def Explore(self):
        self.explored = True
    
    def Update(self, gCost:int, hCost:int):
        if gCost < self.gCost:
            self.gCost = gCost
        self.hCost = hCost
    
    def Cost(self):
        return self.gCost + self.hCost