from classes.Character import Character
from classes.Position import Position
from classes.Weapon import Weapon

class Monster(Character):
    def __init__(self, name:str="Moveable", description:str="Lorem Ipsum", imageLink:str="./assets/carreblanc.png", healthPoints:int=0, position:Position=Position(0,0), movementPoints:int=0, weapon:Weapon=Weapon([[0]],Position(0,0))):
        super().__init__(name, description, imageLink, healthPoints, position, movementPoints, weapon)

