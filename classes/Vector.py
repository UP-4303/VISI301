from __future__ import annotations
from typing import Any
from math import sqrt

class Vector():
    x:int
    y:int

    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y

    def CollinearToAxis(self):
        return self.x == 0 or self.y == 0

    def Normalize(self):
        if abs(self) == 0:
            return Vector(0,0)
        else:
            return Vector(int(self.x/abs(self)), int(self.y/abs(self)))

    def __mul__(self, multiplier:int):
        return Vector(self.x*multiplier, self.y*multiplier)
    
    def __abs__(self):
        return sqrt((self.x**2) + (self.y**2))

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