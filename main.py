from distutils.spawn import spawn
from unittest import IsolatedAsyncioTestCase
import pygame

class Board():
    def __init__(self, size:tuple(int,int)):
        # size[0] is the width and size[1] is height
        self.size = size
        self.all = [['' for i in range(self.size[0])] for j in range(self.size[1])]

    def Update(self, coordinates:tuple(int,int), newObject):
        self.all[coordinates[0]][coordinates[1]] = newObject
        return self

    def IsCaseOccupied(self, coordinates:tuple(int,int)):
        return self.all[coordinates[0]][coordinates[1]] == ''

# Classe abstraite parente de tout objet suceptible de bouger
class MovableObject():
    def __init__(self, spawnCoordinates:tuple(int,int)):
        self.coordinates = spawnCoordinates
        if globalBoard.IsCaseOccupied(self.coordinates):
            self.__del__()
        else:
            globalBoard.Update((self.coordinates[0],self.coordinates[1]), self)
    
    def __del__(self):
        print('Succesfully deleted')

    def MoveUp(self):
        if not globalBoard.IsCaseOccupied((self.coordinates[0],self.coordinates[1]+1)):
            globalBoard.Update(self.coordinates) == ''
            self.coordinates[1] += 1
            globalBoard.Update(self.coordinates) == self
        

if __name__ == '__main__':
    global globalBoard
    globalBoard = Board((10,10))