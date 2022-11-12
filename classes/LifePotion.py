from classes.PickableObject import PickableObject
from classes.Player import Player

class Money(PickableObject):

    def __init__(self, position:Position=Position(0,0)):
        super().__init__("Life potion", "Potion that make you recover one point of life", "./assests/lifepotion.png", 2, position)


    def ispicked(self, Player):
        Player.RecoverHealth(1)




