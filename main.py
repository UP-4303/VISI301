import pygame

from classes.Board import Board as Board
from classes.Player import Player as Player
from classes.Position import Position as Position
from classes.UnmovableObject import UnmovableObject as UnmovableObject
from classes.Vector import Vector as Vector

if __name__ == '__main__':
    # Ici s'exécutera le code principal. Pour l'instant, contient les codes de test.
    board = Board((5,5))
    player = Player(Position(1,1), board)
    print(board.all)
    player.Move(Vector(1,0))
    print(board.all)
    player.TakeDamage(9)
    player.PlayTurn()
    print(board.all)