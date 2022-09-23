import pygame

from classes.Board import Board
from classes.Monster import Monster
from classes.Player import Player
from classes.Position import Position
from classes.Bloc import Bloc
from classes.Vector import Vector

if __name__ == '__main__':
    # Ici s'exécutera le code principal. Pour l'instant, contient les codes de test.
    board = Board((10,10))
    toUpdate = []
    player = Player(Position(1,1), board)
    toUpdate.append(player)
    monster = Monster(Position(1,6), board)
    toUpdate.append(monster)
    monster2 = Monster(Position(1,3), board)
    toUpdate.append(monster2)

    bloc1 = Bloc(Position())

    print(board.all)

    for i in range(3):
        for updatingObject in toUpdate:
            updatingObject.PlayTurn()
        print(board.all)