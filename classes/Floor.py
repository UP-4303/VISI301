from __future__ import annotations
from typing import Any, TypedDict
from math import inf
import pygame

from classes.GenericObject import GenericObject
from classes.Monster import Monster
from classes.Player import Player
from classes.Position import Position
from classes.Size import Size


class Floor():
    name:str
    size:Size
    layers:dict[str, Any]
    playerGroup:pygame.sprite.Group
    monsterGroup:pygame.sprite.Group

    def __init__(self, name:str="Floor 0", size:Size=Size(6,6)):
        self.name = name
        self.size = size

        self.layers = {
            "objects": [[None for _y in range(self.size.height)] for _x in range(self.size.width)]
        }

        self.playerGroup = pygame.sprite.Group()
        self.monsterGroup = pygame.sprite.Group()
    
    def GetObject(self, position:Position):
        return self.layers["objects"][position.x][position.y]


# Ajoute un object

    def SetNewObject(self, position:Position, object_:GenericObject):
        if self.GetObject(position) == None:
            self.layers["objects"][position.x][position.y] = object_
            object_.position = position

            if isinstance(object_, Player):
                self.playerGroup.add(object_)
            if isinstance(object_, Monster):
                self.monsterGroup.add(object_)
            return True
        else:
            return False
    
    def UpdateObject(self, position:Position, newPosition:Position):
        if self.GetObject(newPosition) == None:
            object_ = self.GetObject(position)
            self.layers["objects"][newPosition.x][newPosition.y] = object_
            object_.position = newPosition
            self.layers["objects"][position.x][newPosition.y] = None
            return True
        else:
            return False
    
    def RemoveObject(self, position:Position):
        if self.GetObject(position)!= None:
            object_ = self.GetObject(position)
            if isinstance(object_, Player):
                self.playerGroup.remove(object_)
            if isinstance(object_, Monster):
                self.monsterGroup.remove(object_)
            self.layers["objects"][position.x][position.y] = None
            return True
        else:
            return False

    def UpdatePlayer(self, player:Player, destination:Position):
        path = self.Pathfinder(player.position, destination)
        if path != []:
            movementPoints = player.movementPoints
            if movementPoints > 0:
                index = 0
                currentPosition = path[index]
                while index < len(path)-1 and movementPoints >= currentPosition["bias"]:
                    movementPoints -= currentPosition["bias"]
                    index += 1
                    currentPosition = path[index]
                self.UpdateObject(player.position, path[index]["position"])

    def UpdateMonster(self, monster:Monster):
        pass

    def Pathfinder(self, actualPosition:Position, targetPosition:Position):
        PathPoint = TypedDict('PathPoint', position=Position, bias=float)
        path:list[PathPoint] = []
        nodes:list[list[Node]] = [[Node(x,y,targetPosition, inf if self.GetObject(Position(x,y)) != None else 1, Position(x,y) == actualPosition) for y in range(self.size.height)] for x in range(self.size.width)]
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