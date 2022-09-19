from classes.Board import Board
from classes.Position import Position
from classes.Vector import Vector

from utils.Pathfinder import PathfinderMonster as Pathfinder

class Monster():
    def __init__(self, spawnCoordinates:Position, board:Board):
        # Attributes
        self.coordinates = spawnCoordinates
        self.board = board
        self.healthPoints = 9
        self.movePoints = 3

        # Treating creation on board
        if self.board.IsCaseOccupied(self.coordinates):
            self.__del__("SPAWN CASE ALREADY OCCUPIED")
        else:
            self.board.NewObject(self.coordinates, self)

    # Delete the monster and print a message for debug purpose
    def __del__(self, reason:str="Monster deleted"):
        print(reason)

    # Delete the monster and it's board self. Don't call this method if the monster is not on the board
    def DelFromBoard(self, reason:str):
        self.board.DeleteObject(self.coordinates)
        self.__del__(reason)

    # Just move the monster. USE IT CAUTIOUSLY (it can delete another object on the board)
    def Move(self):
        moveTo = Pathfinder(self.board, self)
        self.board.MoveObject(self.coordinates, moveTo)
        self.coordinates.Move(moveTo - self.coordinates)

    # Decrease health
    def TakeDamage(self, amount:int):
        self.healthPoints -= amount

    # Increase health
    def RecoverHealth(self, amount:int):
        self.healthPoints += amount
    
    # The main code of the monster, that will be called every turn (actually just check the health)
    def PlayTurn(self):
        # Check health. If the monster is dead, it will be deleted. Else, play normally
        if self.healthPoints <= 0:
            self.DelFromBoard('MONSTER IS DEAD')
        else:
            self.Move()