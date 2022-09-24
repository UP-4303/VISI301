from classes.Board import Board
from classes.Position import Position

from utils.Pathfinder import Pathfinder

class Monster():
    def __init__(self, spawnCoordinates:Position, board:Board, uncrossableTypes:list, targetingFunction):
        # Attributes
        self.coordinates = spawnCoordinates
        self.board = board
        self.healthPoints = 9
        self.movePoints = 3
        self.uncrossableTypes = uncrossableTypes

        self.TargetingFunction = targetingFunction

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

    # Use pathfinding to go to the nearest target position
    def Move(self):
        targets = self.TargetingFunction(self)
        if targets != []:
            path = Pathfinder(self.board, self, targets, self.uncrossableTypes)
            movePoints = self.movePoints
            newCoordinates = path.value[min(movePoints, len(path.value)-1)].coordinates
            while self.board.get(newCoordinates) != None and self.board.get(newCoordinates) != self:
                movePoints -= 1
                newCoordinates = path.value[min(movePoints, len(path.value)-1)].coordinates
            self.board.MoveObject(self.coordinates, newCoordinates)
            self.coordinates = newCoordinates

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