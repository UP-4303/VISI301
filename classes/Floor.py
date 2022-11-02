from __future__ import annotations
from typing import Any, TypedDict
from math import inf
from random import randint
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
            self.layers["objects"][position.x][position.y] = None
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
        # print(path, destination)
        sumCost = 0
        for currentNode in path:
            sumCost += currentNode["bias"]
        if sumCost <= player.movementPoints and sumCost != 0:
            self.UpdateObject(player.position, path[-1]["position"])
        else:
            print("Chemin trop long ou inexistant !")

    def UpdateMonster(self, monster:Monster):
        allTargets = []
        for xBoard in range(self.size.width):
            for yBoard in range(self.size.height):
                for xPattern in range(len(monster.weapon.pattern)):
                    for yPattern in range(len(monster.weapon.pattern[xPattern])):
                        position = Position(xBoard + xPattern - monster.weapon.center.x, yBoard + yPattern - monster.weapon.center.y)
                        if position.InBoard(self.size):
                            if isinstance(self.GetObject(position), Player) and monster.weapon.pattern[xPattern][yPattern] > 0:
                               allTargets.append(Position(xBoard, yBoard))
        
        completePaths = []
        partialPaths = []
        for target in allTargets:
            path = self.Pathfinder(monster.position, target)
            if path != []:
                pathLenght = 0
                for node in path:
                    pathLenght += node['bias']
                if pathLenght <= monster.movementPoints:
                    completePaths.append(path)
                elif path[0]['bias'] <= monster.movementPoints:
                        partialPaths.append(path)
        if completePaths != []:
            self.UpdateObject(monster.position, completePaths[randint(0,len(completePaths)-1)][-1]["position"])
        elif partialPaths != []:
            pathIndex = randint(0,len(partialPaths)-1)
            positionIndex = 0
            pathLenght = partialPaths[pathIndex][positionIndex]['bias']
            while pathLenght + partialPaths[pathIndex][positionIndex+1]['bias'] <= monster.movementPoints:
                positionIndex += 1
                pathLenght += partialPaths[pathIndex][positionIndex]['bias']
            self.UpdateObject(monster.position, partialPaths[pathIndex][positionIndex]["position"])

    def Pathfinder(self, actualPosition:Position, targetPosition:Position):
        PathPoint = TypedDict('PathPoint', position=Position, bias=float)
        path:list[PathPoint] = []
        nodes:list[list[Node]] = [[Node(x,y,targetPosition, inf if self.GetObject(Position(x,y)) != None else 1, Position(x,y) == actualPosition) for y in range(self.size.height)] for x in range(self.size.width)]
        nodesToExplore = ToExplore()

        # for x in range(self.size.width):
        #     for y in range(self.size.height):
        #         print(nodes[x][y].bias)
        
        currentNode = nodes[actualPosition.x][actualPosition.y]
        
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
            # print("current node : ", currentNode, currentNode.bias)
            # print("To explore :", nodesToExplore)
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
    
    def PathLength(self, path):
        length = 0
        for pathPoint in path:
            length += pathPoint['bias']
        return length

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
        if self.start:
            self.gCost = 0
            self.explored = True

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