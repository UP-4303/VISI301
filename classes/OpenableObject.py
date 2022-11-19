from classes.Player import Player
from classes.StaticObject import StaticObject
from classes.Position import Position
from classes.Monster import Monster

class OpenableObject(StaticObject):

    def __init__(self, name:str="Static", description:str="Lorem Ipsum", imageLink:str="./assets/carreblanc.png", healthPoints:int=0, position:Position=Position(0,0)):
        super().__init__(name, description, imageLink, healthPoints, position)
        self.isNowOpen = False


    def isOpen(self, Player):
        Player.score += 5


    def showInside(self, screen) :
        print("you want to show inside")





    def isCrushed(self, Monster):
        self.healthPoints = self.healthPoints - 1
