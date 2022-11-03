from classes.Position import Position
from classes.MoveableObject import MoveableObject
from classes.Weapon import Weapon

class Character(MoveableObject):
    weapon:Weapon
    def __init__(self, name:str="Moveable", description:str="Lorem Ipsum", imageLink:str="./assets/carreblanc.png", healthPoints:int=0, position:Position=Position(0,0), movementPoints:int=0, weapon:Weapon=Weapon()):
        super().__init__(name, description, imageLink, healthPoints, position, movementPoints)
        self.weapon = weapon