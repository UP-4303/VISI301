from math import inf

from classes.Board import Board
from classes.Bloc import Bloc
from classes.Node import Node
from classes.NodeList import NodeList
from classes.Player import Player
from classes.Position import Position
from classes.Vector import Vector

# For the pathfinder, we will use an adapted A* algorithm for cardinal neighborhood
# This function return a path object (which is a list of positions)
def Pathfinder(board:Board, object, targets:list, uncrossableTypes:list):
    nodeList = NodeList(board, uncrossableTypes, object.coordinates)

    nodeList[monster.coordinates.y][monster.coordinates.x].Update(0, HeuristicCost(targets, monster.coordinates), monster.coordinates, True)
    nodeList[monster.coordinates.y][monster.coordinates.x].Explore()
    if nodeList[monster.coordinates.y][monster.coordinates.x].hCost == 0:
        pathFound = True
    else:
        pathFound = False
        nodeToExplore = []
        
        if monster.coordinates.x > 0:
            nodeList[monster.coordinates.y][monster.coordinates.x-1].Update(1, HeuristicCost(targets, monster.coordinates + Vector(-1,0)), monster.coordinates)
            nodeToExplore.append(monster.coordinates + Vector(-1,0))
        if monster.coordinates.x < board.size[0]-1:
            nodeList[monster.coordinates.y][monster.coordinates.x+1].Update(1, HeuristicCost(targets, monster.coordinates + Vector(1,0)), monster.coordinates)
            nodeToExplore.append(monster.coordinates + Vector(1,0))
        if monster.coordinates.y > 0:
            nodeList[monster.coordinates.y-1][monster.coordinates.x].Update(1, HeuristicCost(targets, monster.coordinates + Vector(0,-1)), monster.coordinates)
            nodeToExplore.append(monster.coordinates + Vector(0,-1))
        if monster.coordinates.y < board.size[1]-1:
            nodeList[monster.coordinates.y+1][monster.coordinates.x].Update(1, HeuristicCost(targets, monster.coordinates + Vector(0, 1)), monster.coordinates)
            nodeToExplore.append(monster.coordinates + Vector(0,1))
    
    while not(pathFound):
        currentNode = NextNode(nodeList, nodeToExplore)
        nodeToExplore.remove(currentNode)
        nodeList[currentNode.y][currentNode.x].Explore()
        if nodeList[currentNode.y][currentNode.x].hCost == 0:
            pathFound = True
        else:
            if currentNode.x > 0:
                nodeList[currentNode.y][currentNode.x-1].Update(nodeList[currentNode.y][currentNode.x].gCost + 1, HeuristicCost(targets, currentNode + Vector(-1,0)), currentNode)
                nodeToExplore.append(currentNode + Vector(-1,0))
            if currentNode.x < board.size[0]-1:
                nodeList[currentNode.y][currentNode.x+1].Update(nodeList[currentNode.y][currentNode.x].gCost + 1, HeuristicCost(targets, currentNode + Vector(1,0)), currentNode)
                nodeToExplore.append(currentNode + Vector(1,0))
            if currentNode.y > 0:
                nodeList[currentNode.y-1][currentNode.x].Update(nodeList[currentNode.y][currentNode.x].gCost + 1, HeuristicCost(targets, currentNode + Vector(0,-1)), currentNode)
                nodeToExplore.append(currentNode + Vector(0,-1))
            if currentNode.y < board.size[1]-1:
                nodeList[currentNode.y+1][currentNode.x].Update(nodeList[currentNode.y][currentNode.x].gCost + 1, HeuristicCost(targets, currentNode + Vector(0,1)), currentNode)
                nodeToExplore.append(currentNode + Vector(0,1))
    return currentNode

# Return the coordinates of the next node to explore
def NextNode(nodeList:list, nodeToExplore:list):
    nextNode = nodeToExplore[0]
    for coordinates in nodeToExplore[1:]:
        if nodeList[coordinates.y][coordinates.x].Cost() < nodeList[nextNode.y][nextNode.x].Cost():
            nextNode = coordinates
        elif nodeList[coordinates.y][coordinates.x].Cost() == nodeList[nextNode.y][nextNode.x].Cost():
            if nodeList[coordinates.y][coordinates.x].hCost < nodeList[nextNode.y][nextNode.x].hCost:
                nextNode = coordinates
    return nextNode

# Calculate the lowest heuristic cost
def HeuristicCost(targets:list, position:Position):
    hCosts = []
    for target in targets:
        hCosts.append(abs(target - position))
    return min(hCosts)