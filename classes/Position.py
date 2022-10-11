from __future__ import annotations
from typing import Any
from classes.Size import Size
from classes.Vector import Vector

class Position():
    x:int
    y:int

    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y
    
    # Move the coordinates
    def Move(self, movement:Vector):
        self.x += movement.x
        self.y += movement.y

    # Check if this position is in the board. Use Floor.size as argument.
    def InBoard(self, size:Size):
        return self.x >= 0 and self.y >= 0 and self.x < size.width and self.y < size.height

    def __eq__(self, other:Any):
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y
        else:
            return False

    def __ne__(self, other:Any):
        return not self.__eq__(other)

    def __add__(self, movement:Vector):
        return Position(self.x + movement.x, self.y + movement.y)
    
    # Vector from other to self
    def __sub__(self, other:Position):
        return Vector(self.x - other.x, self.y - other.y)

    def __repr__(self):
        return f'Position(x={self.x}, y={self.y})'