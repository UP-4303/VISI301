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
            print("BLOC : SPAWN CASE ALREADY OCCUPIED")
        else:
            self.board.NewObject(self.coordinates, self)
    # Delete the bloc on the board. Don't call this method if the bloc is not on the board
    def DelFromBoard(self,reason:str):
        self.board.DeleteObject(self.coordinates)
        print(f"BLOC : {reason}")
    
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