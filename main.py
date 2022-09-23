import pygame

from classes.Board import Board as Board
from classes.MovableObject import MovableObject as MovableObject
from classes.Position import Position as Position
from classes.UnmovableObject import UnmovableObject as UnmovableObject
from classes.Vector import Vector as Vector

if __name__ == '__main__':
    game = Game()
    game.printQuote()



#------------------ Premier test de grille----------------#

#     INIT     #
import pygame
import sys
import random
pygame.init()
game_on = True #on creer une variable booléen pour que la fenetre reste ouverte

#   CST   #

NB_COL = 10
NB_ROW = 15
CELL_SIZE = 40

screen = pygame.display.set_mode(size=(NB_COL * CELL_SIZE, NB_ROW * CELL_SIZE))

timer = pygame.time.Clock()

#fonction pour afficher la grille
def show_grid():
    for i in range(0, NB_COL):
        for j in range(0, NB_ROW):
            rect = pygame.Rect(i*CELL_SIZE, j*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, pygame.Color("black"), rect, width= 1)

def convert_px_in_number(px):
    nb_case = px//CELL_SIZE
    return nb_case



#on creer notre game loop
while game_on:
    for event in pygame.event.get():
        # ferme le jeu quand on le quitte
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # on ajoute l'evenement qui correspond au clic droit
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            #obtenir la position de la souris
            position = pygame.mouse.get_pos()
            #On convertit en coordonées de case
            position_x = convert_px_in_number(position[0])
            position_y = convert_px_in_number(position[1])
            print(position_x, position_y)

    screen.fill(pygame.Color("white"))  # on change la couleur de l'element
    show_grid()
    pygame.display.update()  # met a jour la fenetre et redessine les elements
    timer.tick(60)  # duree du game loop


    # Ici s'exécutera le code principal. Pour l'instant, contient les codes de test.
    board = Board((2,10))
    player = MovableObject(Position(1,1), board)
    print(board.all)
    player.MoveDown()
    print(board.all)
    player.MoveLeft()
    print(board.all)

