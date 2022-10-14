from classes.Character import Character
from classes.Position import Position
from classes.Weapon import Weapon

class Monster(Character):
    #x et y pas top
    def __init__(self, name:str="Moveable", description:str="Lorem Ipsum", imageLink:str="./assets/monster.png", healthPoints:int=100, position: Position =Position(0,0), movementPoints:int=0, weapon:Weapon=Weapon([[0]],Position(0,0))):
        super().__init__(name, description, imageLink, healthPoints, position, movementPoints, weapon)

        #TEST
        self.rect.x = 200
        self.rect.y = 100



