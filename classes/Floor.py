from __future__ import annotations
from typing import Any, TypedDict
from math import inf

from classes.GenericObject import GenericObject
from classes.Monster import Monster
from classes.Player import Player
from classes.Position import Position
from classes.Size import Size


class Floor():
    name:str
    size:Size
    layers:dict[str, Any]
    objects:list[GenericObject]

    def __init__(self, name:str="Floor 0", size:Size=Size(0,0)):
        self.name = name
        self.size = size

        self.layers = {
            "objects": [[None for _y in range(self.size.height)] for _x in range(self.size.width)]
        }
    
    def GetObject(self, position:Position):
        return self.layers["objects"][position.x][position.y]

    def SetNewObject(self, position:Position, object_:Any):
        if self.GetObject(position) == None:
            self.layers["objects"][position.x][position.y] = object_
            object_.position = position
            self.objects.append(object_)
            return True
        else:
            return False
    
    def UpdateObject(self, position:Position, newPosition:Position):
        if self.GetObject(newPosition) == None:
            self.layers["objects"][newPosition.x][newPosition.y] = self.GetObject(position)
            self.GetObject(newPosition).position = newPosition
            self.layers["objects"][position.x][newPosition.y] = None
            return True
        else:
            return False
    
    def RemoveObject(self, position:Position):
        if self.GetObject(position)!= None:
            self.objects.remove(self.GetObject(position))
            self.layers["objects"][position.x][position.y] = None
            return True
        else:
            return False

    def UpdateAll(self):
        for i in self.objects:
            if isinstance(i, Player):
                self.UpdatePlayer(i)
        for i in self.objects:
            if isinstance(i, Monster):
                self.UpdateMonster(i)
        for i in self.objects:
            if i.IsDead():
                self.RemoveObject(i.position)
                self.objects.remove(i)

    def UpdatePlayer(self, player:Player):
        requestedNewPosition = NotImplemented
        path = self.Pathfinder(player.position, requestedNewPosition)
        if path != []:
            movementPoints = player.movementPoints
            index = 0
            currentPosition = path[index]
            while index < len(path)-1 and movementPoints >= currentPosition["bias"]:
                movementPoints -= currentPosition["bias"]
                index += 1
                currentPosition = path[index]
            if movementPoints >= currentPosition["bias"]:
                index += 1
            self.UpdateObject(player.position, path[index]["position"])
            player.position = path[index]["position"]

    def UpdateMonster(self, monster:Monster):
        pass

    def Pathfinder(self, actualPosition:Position, targetPosition:Position):
        PathPoint = TypedDict('PathPoint', position=Position, bias=float)
        path:list[PathPoint] = []
        nodes:list[list[Node]] = [[Node(x,y,targetPosition, inf if self.GetObject(Position(x,y)) != None else 0, Position(x,y) == actualPosition) for y in range(floor.size.height)] for x in range(floor.size.width)]
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
                path.insert(0, {"position":Position(currentNode.x, currentNode.y), "bias":currentNode.bias})
                currentNode = currentNode.pointer

        return path

    def __str__(self):
        representation = '+'
        for _x in range(self.size.width):
            representation += '-'
        representation += '+'
        representation += '\n'
        
        for y in range(self.size.height):
            representation += '|'
            for x in range(self.size.width):
                object_ = self.layers['objects'][x][y]
                if object_ is None:
                    representation += ' '
                elif object_.name == "Bloc":
                    representation += 'B'
                elif object_.name == "Player":
                    representation += 'P'
            representation += '|'
            representation += '\n'

        representation += '+'
        for _x in range(self.size.width):
            representation += '-'
        representation += '+'
        return representation

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