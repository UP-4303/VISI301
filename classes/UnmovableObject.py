from classes.Board import Board as Board
from classes.Position import Position as Position

# Classe abstaite parente de tout les objets immobiles (murs, coffres, portes...)
class UnmovableObject():
    def __init__(self, coordinates:Position, board:Board):
        self.coordinates = coordinates
        self.board = board
        if self.board.IsCaseOccupied(self.coordinates):
            self.__del__()
        else:
            self.board.Update(self.coordinates, self)
            
    def __del__(self):
        print("UnmovableObject succesfully deleted")