import pygame
import sys
from classes.Game import Game

pygame.init()

#Generate the window of the game

pygame.display.set_caption("Our game")
screen = pygame.display.set_mode((1080,720)) # define the dimention of the window



#download the game
game = Game()

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1080, 720))
    clock = pygame.time.Clock()
    background = pygame.image.load('assets/bg.jpg') #import background

    running = True #indicate  if the game is running

    while running:
        screen.blit(background, (0, 0))
        running = game.update(screen)
        # update screen
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

