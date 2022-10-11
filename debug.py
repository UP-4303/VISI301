from classes.BlocObject import BlocObject
from classes.Floor import Floor
from classes.GenericObject import GenericObject
from classes.MovableObject import MoveableObject
from classes.Position import Position
from classes.Size import Size
from classes.StaticObject import StaticObject
from classes.Vector import Vector

f = Floor(size=Size(4,5))
b = BlocObject(position=Position(3,2))
f.layers['objects'][3][2] = b
print(f)