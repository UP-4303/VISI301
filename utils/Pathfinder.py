from classes.Board import Board
from classes.Bloc import Bloc
from classes.Monster import Monster
from classes.Player import Player
from classes.Position import Position
from classes.Vector import Vector

# For the pathfinder, we will use the A* algorithm
def PathfinderMonster(board:Board, monster:Monster):
    targets = []
    for x in range(board.size.x):
        for y in range(board.size.y):
            if board.SelectPosition(Position(x,y)):
                targets.append(Position(x,y))
    

# Define if a position is a valid target
def ValidTargetMonster(board:Board, coordinates:Position):
    check = []
    if coordinates.x > 0:
        check.append(type(board.SelectPosition(coordinates + Vector(-1,0))))
    if coordinates.x < board.size.x:
        type(board.SelectPosition(coordinates + Vector(1,0)))
    if coordinates.y > 0:
        type(board.SelectPosition(coordinates + Vector(0,-1)))
    if coordinates.y < board.size.y:
        type(board.SelectPosition(coordinates + Vector(0,1)))
    return Player in check