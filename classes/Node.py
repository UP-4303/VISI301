from math import nan

from classes.Position import Position

class Node():
    def __init__(self, coordinates:Position, crossable:bool, start:bool=False, explored:bool=False, gCost:int=nan, hCost:int=nan):
        self.coordinates = Position()
        self.explored = explored
        self.gCost = gCost
        self.hCost = hCost
        self.pointToNode:Position
        self.start = start

    def Explore(self):
        self.explored = True
    
    def Update(self, gCost:int, pointToNode:Position):
        if gCost < self.gCost:
            self.gCost = gCost
        self.pointToNode = pointToNode
    
    def Cost(self):
        return self.gCost + self.hCost