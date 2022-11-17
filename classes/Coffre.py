from classes.PickableObject import PickableObject
from classes.Player import Player
from classes.OpenableObject import OpenableObject
from classes.Position import Position
from classes.Weapon import Weapon

class Coffre(OpenableObject):


    def __init__(self, position:Position=Position(0,0),insideTheBox: list = [] ):
        super().__init__("Coffre", "Box containes weapons or pickable", "./assets/coffre.png", 4, position)
        self.insideTheBox=insideTheBox

    def isOpen(self, Player):
        weapons = []
        for object_ in self.insideTheBox:
            if isinstance(object_, PickableObject):
                object_.ispicked(Player)
            elif isinstance(object_, Weapon):
                weapons += object_
        return weapons

    def showInside(self):
        print("you want to show inside")








