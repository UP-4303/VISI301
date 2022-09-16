from classes.Board import Board
from classes.Bloc import Bloc
from classes.Monster import Monster
from classes.Player import Player
from classes.Position import Position
from classes.Vector import Vector

# For the pathfinder, we will use the A* algorithm
def PathfinderMonster(board:Board, monster:Monster):
    pass

def ValidTargetMonster(board:Board, position:Position):
    return Player in [type(position.MovePreview(Vector(1,0))),type(position.MovePreview(Vector(-1,0))),type(position.MovePreview(Vector(0,1))),type(position.MovePreview(Vector(0,-1)))]