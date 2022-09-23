from classes.Board import Board
from classes.Position import Position

# A bloc can't move, but can be destroyed
class Bloc():
    def __init__(self, coordinates:Position, board:Board):
        # Attributes
        self.coordinates = coordinates
        self.board = board
        self.healthPoints = 2

        # Treating creation on board
        if self.board.IsCaseOccupied(self.coordinates):
            self.__del__("SPAWN CASE ALREADY OCCUPIED")
        else:
            self.board.NewObject(self.coordinates, self)
            
    # Delete the bloc and print a message for debug purpose
    def __del__(self, reason:str="Bloc deleted"):
        print(reason)

    # Delete the bloc and it's board self. Don't call this method if the bloc is not on the board
    def DelFromBoard(self,reason:str):
        self.board.DeleteObject(self.coordinates)
        self.__del__(reason)
    
    # Decrease health
    def TakeDamage(self, amount:int):
        self.healthPoints -= amount

    # Increase health
    def RecoverHealth(self, amount:int):
        self.healthPoints += amount
    
    # In it's turn, the bloc just check if it's alive
    def PlayTurn(self):
        # Check health. If the bloc is dead, it will be deleted
        if self.healthPoints <= 0:
            self.DelFromBoard('BLOC IS DEAD')