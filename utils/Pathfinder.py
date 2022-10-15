from __future__ import annotations

from classes.Position import Position
from classes.Floor import Floor

from math import inf

def Pathfinder(actualPosition:Position, targetPosition:Position, floor:Floor):
    path:list[Position] = []
    nodes:list[list[Node]] = [[Node(x,y,targetPosition, inf if floor.GetObject(Position(x,y)) != None else 0, Position(x,y) == actualPosition) for y in range(floor.size.height)] for x in range(floor.size.width)]
    nodesToExplore = ToExplore()
    
    currentNode = nodes[actualPosition.x][actualPosition.y]

    currentNode.Discover(0, currentNode)
    
    currentNode.Explore()
    if currentNode.x > 0:
        addingNode = nodes[currentNode.x-1][currentNode.y]
        addingNode.Discover(currentNode.gCost+1, currentNode)
        if not(addingNode.explored) and not(addingNode in nodesToExplore):
            nodesToExplore.append(addingNode)
    if currentNode.y > 0:
        addingNode = nodes[currentNode.x][currentNode.y-1]
        addingNode.Discover(currentNode.gCost+1, currentNode)
        if not(addingNode.explored) and not(addingNode in nodesToExplore):
            nodesToExplore.append(addingNode)
    if currentNode.x < len(nodes)-1:
        addingNode = nodes[currentNode.x+1][currentNode.y]
        addingNode.Discover(currentNode.gCost+1, currentNode)
        if not(addingNode.explored) and not(addingNode in nodesToExplore):
            nodesToExplore.append(addingNode)
    if currentNode.y < len(nodes[0])-1:
        addingNode = nodes[currentNode.x][currentNode.y+1]
        addingNode.Discover(currentNode.gCost+1, currentNode)
        if not(addingNode.explored and not(addingNode in nodesToExplore)):
            nodesToExplore.append(addingNode)
    
    while nodesToExplore!= [] and Position(currentNode.x, currentNode.y) != targetPosition :
        currentNode = nodesToExplore.pop(-1)
        currentNode.Explore()
        if currentNode.gCost != inf:
            if currentNode.x > 0:
                addingNode = nodes[currentNode.x-1][currentNode.y]
                addingNode.Discover(currentNode.gCost+1, currentNode)
                if not(addingNode.explored) and not(addingNode in nodesToExplore):
                    nodesToExplore.append(addingNode)
            if currentNode.y > 0:
                addingNode = nodes[currentNode.x][currentNode.y-1]
                addingNode.Discover(currentNode.gCost+1, currentNode)
                if not(addingNode.explored) and not(addingNode in nodesToExplore):
                    nodesToExplore.append(addingNode)
            if currentNode.x < len(nodes)-1:
                addingNode = nodes[currentNode.x+1][currentNode.y]
                addingNode.Discover(currentNode.gCost+1, currentNode)
                if not(addingNode.explored) and not(addingNode in nodesToExplore):
                    nodesToExplore.append(addingNode)
            if currentNode.y < len(nodes[0])-1:
                addingNode = nodes[currentNode.x][currentNode.y+1]
                addingNode.Discover(currentNode.gCost+1, currentNode)
                if not(addingNode.explored) and not(addingNode in nodesToExplore):
                    nodesToExplore.append(addingNode)
    
    if Position(currentNode.x, currentNode.y) == targetPosition:
        while not(currentNode.start):
            path.insert(0, Position(currentNode.x, currentNode.y))
            currentNode = currentNode.pointer

    return path

class Node(Position):
    hCost: int
    gCost: float
    bias: float # Some nodes are harder to reach. It's a float and not an int so we can use inf
    explored: bool = False
    pointer: Node
    start: bool

    def __init__(self, x:int, y:int, targetPosition:Position, bias:float=0, start=False):
        super().__init__(x,y)
        self.hCost = abs(targetPosition - self)
        self.bias = bias
        self.start = start

    def Discover(self, gCost:float, pointer:Node):
        if self.explored:
            if gCost+self.bias < self.gCost:
                self.gCost = gCost + self.bias
                self.pointer = pointer
                self.explored = False
        else:
            self.gCost = gCost + self.bias
            self.pointer = pointer
    
    def Explore(self):
        self.explored = True
    
    def Cost(self):
        return self.gCost + self.hCost
        

class ToExplore(list[Node]):
    def __init__(self):
        super().__init__()
    
    def append(self, node:Node):
        if len(self) == 0:
            super().append(node)
        else:
            checkingIndex = 0
            checkingNode = self[checkingIndex]
            while checkingIndex < len(self)-1 and (checkingNode.Cost() > node.Cost() or checkingNode.Cost() == node.Cost() and checkingNode.hCost > node.hCost):
                checkingIndex += 1
                checkingNode = self[checkingIndex]
            if (checkingNode.Cost() > node.Cost() or checkingNode.Cost() == node.Cost() and checkingNode.hCost > node.hCost):
                super().append(node)
            else:
                self.insert(checkingIndex, node)