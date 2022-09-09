from data.Board import Board as Board
from data.Vector import Vector as Vector
from data.Vector import Position as Position

# Classe abstraite parente de tout objet suceptible de bouger
class MovableObject():
    def __init__(self, spawnCoordinates:Position, board:Board):
        self.coordinates = spawnCoordinates
        self.board = board
        if self.board.IsCaseOccupied(self.coordinates):
            self.__del__()
        else:
            self.board.Update(self.coordinates, self)
    
    def __del__(self):
        print('Succesfully deleted')

    def MoveUp(self):
        if not self.board.IsCaseOccupied(Position(self.coordinates.x-1,self.coordinates.y)):
            self.board.Update(self.coordinates, '')
            self.coordinates.Move(Vector(-1,0))
            self.board.Update(self.coordinates, self)

    def MoveDown(self):
        if not self.board.IsCaseOccupied(Position(self.coordinates.x+1,self.coordinates.y)):
            self.board.Update(self.coordinates, '')
            self.coordinates.Move(Vector(1,0))
            self.board.Update(self.coordinates, self)

    def MoveRight(self):
        if not self.board.IsCaseOccupied(Position(self.coordinates.x,self.coordinates.y+1)):
            self.board.Update(self.coordinates, '')
            self.coordinates.Move(Vector(0,1))
            self.board.Update(self.coordinates, self)
    
    def MoveLeft(self):
        if not self.board.IsCaseOccupied(Position(self.coordinates.x,self.coordinates.y-1)):
            self.board.Update(self.coordinates, '')
            self.coordinates.Move(Vector(0,-1))
            self.board.Update(self.coordinates, self)