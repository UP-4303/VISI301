from classes.PickableObject import PickableObject
from classes.Player import Player
from classes.Position import Position

class Money(PickableObject):

    def __init__(self, position:Position=Position(0,0)):
        super().__init__("Life potion", "Potion that make you recover one point of life", "./assets/lifepotion.png", 2, position)


    def ispicked(self, Player):
        Player.RecoverHealth(1)




