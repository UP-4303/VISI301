import pygame
from data.MovableObject import MovableObject as MovableObject
from data.Board import Board as Board
from data.Vector import Position as Position
from data.Vector import Vector as Vector

if __name__ == '__main__':
    board = Board((2,10))
    player = MovableObject(Position(1,1), board)
    print(board.all)
    player.MoveDown()
    print(board.all)
    player.MoveLeft()
    print(board.all)