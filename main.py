
#     INIT     #
import pygame
import sys
import random

from classes.Board import Board as Board
from classes.Position import Position as Position
from classes.Vector import Vector as Vector

from mainImport import *


import gestiongrille

if __name__ == '__main__':
    pygame.init()
    game_on = True #on creer une variable booléen pour que la fenetre reste ouverte
    
    # Ici s'exécutera le code principal. Pour l'instant, contient les codes de test.
    board = Board((10,10))
    toUpdate = []
    player = Player(Position(1,1), board)
    toUpdate.append(player)
    monster = Monster(Position(1,6), board)
    toUpdate.append(monster)
    monster2 = Monster(Position(1,3), board)
    toUpdate.append(monster2)

    print(board.all)

    for i in range(3):
        for updatingObject in toUpdate:
            updatingObject.PlayTurn()
        print(board.all)



