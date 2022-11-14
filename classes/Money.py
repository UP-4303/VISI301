from classes.PickableObject import PickableObject
from classes.Player import Player
from classes.Position import Position

class Money(PickableObject):

    def __init__(self, position:Position=Position(0,0)):
        super().__init__("Money", "Coin that make you gain 5 dollars", "./assets/money.png", 2, position)


    def ispicked(self, Player):
        Player.money = Player.money + 5