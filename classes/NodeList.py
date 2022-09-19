from classes.Board import Board
from classes.Node import Node
from classes.Position import Position

class NodeList():
    def __init__(self, board:Board, uncrossableTypes:list, objectCoordinates:Position):
        self.all = [[Node(Position(x,y), type(board.get(Position(x,y))) in uncrossableTypes, objectCoordinates == Position(x,y)) for x in range(board.size[0])] for y in range(board.size[1])]
    
    def get(self, coordinates:Position):
        return self.all[coordinates.y][coordinates.x]
    
    def set(self, coordinates:Position, newValue:Node):
        self.all[coordinates.y][coordinates.x] = newValue
