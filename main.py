import pygame

from classes.Board import Board as Board
from classes.Player import Player as Player
from classes.Position import Position as Position
from classes.Bloc import Bloc as Bloc
from classes.Vector import Vector as Vector

if __name__ == '__main__':
    # Ici s'exécutera le code principal. Pour l'instant, contient les codes de test.
    board = Board((5,5))
    toUpdate = []
    player = Player(Position(1,1), board)
    toUpdate.append(player)
    mountain = Bloc(Position(1,2), board)
    toUpdate.append(mountain)
    print(board.all)