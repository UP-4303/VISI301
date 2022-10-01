import pygame

from classes.Bloc import Bloc as Bloc
from classes.Board import Board as Board
from classes.Monster import Monster as Monster
from classes.Player import Player as Player
from classes.Position import Position as Position
from classes.Vector import Vector as Vector

#fonction pour afficher la grille
def show_grid(board, SCREEN, CELL_SIZE):
    for i in range(board.size[0]):
        for j in range(0, board.size[1]):
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

            rect = pygame.draw.rect(SCREEN, color, rect, width=4)

# fonction qui convertie un nombre de pixel en nombre de case
def convert_px_in_number(px, CELL_SIZE):
    nb_case = px//CELL_SIZE
    return nb_case

# Return true if a click is detected
def DetectClick():
    pygame.event.clear()
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    return event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]

def MousePosition():
    return pygame.mouse.get_pos()