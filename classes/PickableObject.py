from classes.Player import Player
from classes.StaticObject import StaticObject

class PickableObject(StaticObject):

    def __init__(self, name:str="Static", description:str="Lorem Ipsum", imageLink:str="./assets/carreblanc.png", healthPoints:int=0, position:Position=Position(0,0)):
        super().__init__(name, description, imageLink, healthPoints, position)


    def ispicked(self, Player):
        Player.score = Player.score + 5











