from math import nan

from classes.Position import Position

class Node():
    def __init__(self, explored:bool=False, gCost:int=nan, hCost:int=nan):
        self.explored = explored
        self.gCost = gCost
        self.hCost = hCost
        self.pointToNode:Position()

    def Explore(self):
        self.explored = True
    
    def Update(self, gCost:int, pointToNode:Position, start:bool=False):
        if gCost < self.gCost:
            self.gCost = gCost
        self.pointToNode = pointToNode
        self.start = start
    
    def Cost(self):
        return self.gCost + self.hCost