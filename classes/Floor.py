from typing import Any

from classes.BlocObject import BlocObject
from classes.Player import Player

from classes.Size import Size

class Floor():
    name:str
    size:Size
    layers:dict[str, Any]

    def __init__(self, name:str="Floor 0", size:Size=Size(0,0)):
        self.name = name
        self.size = size

        self.layers = {
            "objects": [[None for _y in range(self.size.height)] for _x in range(self.size.width)]
        }

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
                elif isinstance(object_, BlocObject):
                    representation += 'B'
                elif isinstance(object_, Player):
                    representation += 'P'
            representation += '|'
            representation += '\n'

        representation += '+'
        for _x in range(self.size.width):
            representation += '-'
        representation += '+'
        return representation