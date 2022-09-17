from math import inf

from classes.Board import Board
from classes.Bloc import Bloc
from classes.Monster import Monster
from classes.PathNode import PathNode
from classes.Player import Player
from classes.Position import Position
from classes.Vector import Vector

# For the pathfinder, we will use an adapted A* algorithm for cardinal neighborhood
def PathfinderMonster(board:Board, monster:Monster):
    targets = []
    nodeList = [[None for i in range(board.size[0])] for j in range(board.size[1])]
    for x in range(board.size[0]):
        for y in range(board.size[1]):
            if ValidTargetMonster(board, board.SelectPosition(Position(x,y))):
                targets.append(Position(x,y))
    
    
    nodeList[monster.coordinates.x][monster.coordinates.y] = PathNode(0, HeuristicCost(targets, monster.coordinates))

# Find the lowest heuristic cost
def HeuristicCost(targets:list, position:Position):
    hCosts = []
    for target in targets:
        hCosts.append(abs(target - position))
    return min(hCosts)


# Define if a position is a valid target
def ValidTargetMonster(board:Board, coordinates:Position):
    check = []
    if coordinates.x > 0:
        check.append(type(board.SelectPosition(coordinates + Vector(-1,0))))
    if coordinates.x < board.size.x:
        check.append(type(board.SelectPosition(coordinates + Vector(1,0))))
    if coordinates.y > 0:
        check.append(type(board.SelectPosition(coordinates + Vector(0,-1))))
    if coordinates.y < board.size.y:
        check.append(type(board.SelectPosition(coordinates + Vector(0,1))))
    return Player in check