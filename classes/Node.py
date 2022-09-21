from math import nan

from classes.Position import Position

class Node():
    def __init__(self, coordinates:Position, uncrossable:bool, start:bool=False, explored:bool=False, gCost:int=-1, hCost:int=-1):
        self.coordinates = coordinates
        self.uncrossable = uncrossable
        self.explored = explored
        self.start = start
        self.gCost = gCost
        self.hCost = hCost
        self.pointToNode:Node

    def Explore(self):
        self.explored = True
    
    def Update(self, gCost:int, pointToNode):
        if gCost < self.gCost or self.gCost == -1:
            self.gCost = gCost
        self.pointToNode = pointToNode
    
    def Cost(self):
        return self.gCost + self.hCost