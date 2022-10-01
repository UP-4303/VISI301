import pygame
import sys
import random

from classes.Position import Position as Position
from classes.Vector import Vector as Vector
from classes.Monster import Monster as Monster
from classes.Player import Player as Player
from classes.Bloc import Bloc as Bloc
pygame.init()
game_on = True #on creer une variable booléen pour que la fenetre reste ouverte

from classes.Board import Board as Board



#   CST   #

NB_COL = 10
NB_ROW = 4
CELL_SIZE = 40

#à retirer ensuite
board = Board((NB_ROW, NB_COL))
##################
screen = pygame.display.set_mode(size=(NB_COL * CELL_SIZE, NB_ROW * CELL_SIZE))

timer = pygame.time.Clock()

#fonction pour afficher la grille
def show_grid(board):
    for i in range(0, NB_COL):
        for j in range(0, NB_ROW):
            rect = pygame.Rect(i*CELL_SIZE, j*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            #rect = pygame.draw.rect(screen, pygame.Color("black"), rect, width= 1)
            pos = Position(i,j)
            color = pygame.Color("black")
            if board.getCase(pos) is None:
                color = pygame.Color("blue")
            if isinstance(board.getCase(pos), Monster):
                color = pygame.Color("green")
            if isinstance(board.getCase(pos), Player):
                color = pygame.Color("Yellow")
            if isinstance(board.getCase(pos), Bloc):
                color = pygame.Color("Red")

            rect = pygame.draw.rect(screen, color, rect, width=4)

# fonction qui convertie un nombre de pixel en nombre de case
def convert_px_in_number(px):
    nb_case = px//CELL_SIZE
    return nb_case

