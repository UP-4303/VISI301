from data.Board import Board as Board
from data.Vector import Vector as Vector

# Classe abstraite parente de tout objet suceptible de bouger
class MovableObject():
    def __init__(self, spawnCoordinates:tuple[int,int], board:Board):
        self.coordinates = spawnCoordinates
        self.board = board
        if self.board.IsCaseOccupied(self.coordinates):
            self.__del__()
        else:
            self.board.Update((self.coordinates[0],self.coordinates[1]), self)
    
    def __del__(self):
        print('Succesfully deleted')

    def MoveUp(self):
        if not self.board.IsCaseOccupied((self.coordinates[0],self.coordinates[1]+1)):
            self.board.Update(self.coordinates, '')
            self.coordinates[1] += 1
            self.board.Update(self.coordinates, self)

    def MoveDown(self):
        if not self.board.IsCaseOccupied((self.coordinates[0],self.coordinates[1]-1)):
            self.board.Update(self.coordinates, '')
            self.coordinates[1] += 1
            self.board.Update(self.coordinates, self)

    def MoveRight(self):
        if not self.board.IsCaseOccupied((self.coordinates[0]+1,self.coordinates[1])):
            self.board.Update(self.coordinates, '')
            self.coordinates[1] += 1
            self.board.Update(self.coordinates, self)
    
    def MoveLeft(self):
        if not self.board.IsCaseOccupied((self.coordinates[0]-1,self.coordinates[1])):
            self.board.Update(self.coordinates, '')
            self.coordinates[1] += 1
            self.board.Update(self.coordinates, self)