from classes.Board import Board as Board
from classes.Position import Position as Position
from classes.Vector import Vector as Vector

class Player():
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

    # Delete the player and print a message for debug purpose
    def __del__(self, reason:str="Player deleted"):
        print(reason)

    def DelFromBoard(self,reason:str):
        self.board.DeleteObject(self.coordinates)
        self.__del__(reason)

    # Just move the player. USE IT CAUTIOUSLY
    def Move(self, vector:Vector):
        self.coordinates.Move(vector)
        self.board.MoveObject(self.coordinates, self.coordinates.MovePreview(vector))
    
    # Check if the destination case is occupied and move only if possible
    def CheckAndMove(self, vector:Vector):
        if not self.board.IsCaseOccupied(self.coordinates.MovePreview(vector)):
            self.Move(vector)
    
    # Decrease health
    def TakeDamage(self, amount:int):
        self.healthPoints -= amount

    # Increase health
    def RecoverHealth(self, amount:int):
        self.healthPoints += amount
    
    # The main code of the player, that will be called every turn (actually just check the health)
    def PlayTurn(self):
        # Check health. If the player is dead, it will be deleted
        if self.healthPoints <= 0:
            self.__del__('PLAYER IS DEAD')