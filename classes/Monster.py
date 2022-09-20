from classes.Bloc import Bloc
from classes.Board import Board
from classes.Player import Player
from classes.Position import Position
from classes.Vector import Vector

from utils.Pathfinder import Pathfinder

class Monster():
    def __init__(self, spawnCoordinates:Position, board:Board):
        # Attributes
        self.coordinates = spawnCoordinates
        self.board = board
        self.healthPoints = 9
        self.movePoints = 3
        self.uncrossableTypes = [Player, Bloc]

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
        path = Pathfinder(self.board, self, self.Targets(), self.uncrossableTypes)

    # Decrease health
    def TakeDamage(self, amount:int):
        self.healthPoints -= amount

    # Increase health
    def RecoverHealth(self, amount:int):
        self.healthPoints += amount

    # Find all movement targets
    def Targets(self):
        targets = []
        # For every cell
        for y in range(self.board.size[1]):
            for x in range(self.board.size[0]):
                # If the cell is empty
                if self.board.get(Position(x,y)) == None:
                    # Check if this cell is a valid target.
                    # Current rule for valid target : If a cell next to the checking cell contains a player, the checking cell is valid. 
                    if x > 0 and type(self.board.get(Position(x-1,y))) == Player:
                        targets.append(Position(x-1,y))
                    elif x < self.board.size[0] and type(self.board.get(Position(x+1,y))) == Player:
                        targets.append(Position(x+1,y))
                    elif y > 0 and type(self.board.get(Position(x,y-1))) == Player:
                        targets.append(Position(x,y-1))
                    elif y < self.board.size[1] and type(self.board.get(Position(x,y+1))) == Player:
                        targets.append(Position(x,y+1))
        return targets

    # The main code of the monster, that will be called every turn (actually just check the health)
    def PlayTurn(self):
        # Check health. If the monster is dead, it will be deleted. Else, play normally
        if self.healthPoints <= 0:
            self.DelFromBoard('MONSTER IS DEAD')
        else:
            self.Move()