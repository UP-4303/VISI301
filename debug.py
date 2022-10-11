from classes.BlocObject import BlocObject
from classes.Floor import Floor
from classes.GenericObject import GenericObject
from classes.MoveableObject import MoveableObject
from classes.Position import Position
from classes.Size import Size
from classes.StaticObject import StaticObject
from classes.Vector import Vector
from classes.Weapon import Weapon

patternTop = [
    [0,1,0],
    [0,0,0],
    [0,0,0]]

patternLeft = [
    [0,0,0],
    [1,0,0],
    [0,0,0]]

patternBottom = [
    [0,0,0],
    [0,0,0],
    [0,1,0]]

patternRight = [
    [0,0,0],
    [0,0,1],
    [0,0,0]]

weaponTop = Weapon(patternTop, Position(1,1))
weaponLeft = Weapon(patternLeft, Position(1,1))
weaponBottom = Weapon(patternBottom, Position(1,1))
weaponRight = Weapon(patternRight, Position(1,1))
weaponNoDamage = Weapon()


########################################################################
#                             TEST ZONE                                #
########################################################################

f = Floor(size=Size(4,5))
b = BlocObject(position=Position(3,2))
f.layers['objects'][3][2] = b
print(f)