import pygame

from classes.Board import Board as Board
from classes.Player import Player as Player
from classes.Position import Position as Position
from classes.UnmovableObject import UnmovableObject as UnmovableObject
from classes.Vector import Vector as Vector

if __name__ == '__main__':
    # Ici s'exécutera le code principal. Pour l'instant, contient les codes de test.
    board = Board((2,10))
    player = Player(Position(1,1), board)
    print(board.all)
    player.MoveDown()
    print(board.all)
    player.MoveLeft()
    print(board.all)