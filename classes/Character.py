from classes.Position import Position
from classes.MovableObject import MoveableObject

class Character(MoveableObject):
    attack:int
    def __init__(self, name:str="Moveable", description:str="Lorem Ipsum", imageLink:str="./assets/carreblanc.png", healthPoints:int=0, position:Position=Position(0,0), movementPoints:int=0, attack:int=10):
        super().__init__(name, description, imageLink, healthPoints, position, movementPoints)
        self.attack = 10




