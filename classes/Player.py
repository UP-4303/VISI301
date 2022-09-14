from classes.Board import Board as Board
from classes.Position import Position as Position
from classes.Vector import Vector as Vector

# Classe abstraite parente de tout objet suceptible de bouger (joueur, monstre, PNJ, projectile...)
class Player():
    def __init__(self, spawnCoordinates:Position, board:Board):
        self.coordinates = spawnCoordinates
        self.board = board
        if self.board.IsCaseOccupied(self.coordinates):
            self.__del__()
        else:
            self.board.Update(self.coordinates, self)
        
        self.healthPoints = 9
        self.movePoints = 3
    
    def __del__(self):
        print('MovableObject succesfully deleted')

    def Move(self, vector:Vector):
        self.coordinates.Move(vector)
        self.board.Move(self.coordinates, self.coordinates.MovePreview(vector))
    
    def CheckAndMove(self, vector:Vector):
        if not self.board.IsCaseOccupied(self.coordinates.MovePreview(vector)):
            self.Move(vector)