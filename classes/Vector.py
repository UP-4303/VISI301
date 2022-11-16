from __future__ import annotations
from typing import Any

class Vector():
    x:int
    y:int

    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y

    def Normalize(self):
        return Vector(int(self.x/self.abs()), int(self.y/self.abs))

    def __mul__(self, multiplier:int):
        return Vector(self.x*multiplier, self.y*multiplier)
    
    def __abs__(self):
        return abs(self.x) + abs(self.y)

    def __eq__(self, other:Any):
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y
        else:
            return False

    def __ne__(self, other:Any):
        return not self.__eq__(other)

    def __add__(self, other:Vector):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other:Vector):
        return Vector(self.x - other.x, self.y - other.y)

    def __repr__(self):
        return f'Vector(x={self.x}, y={self.y})'