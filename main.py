import pygame
import sys
from classes.game import Game

pygame.init()

#Generate the window of the game

pygame.display.set_caption("Our game")
screen = pygame.display.set_mode((1080,720)) # define the dimention of the window

#import background
background = pygame.image.load('assets/bg.jpg')

#download the game
game= Game()

#init player
#player = Player()

running = True #indicate  if the game is running


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1080, 720))
    clock = pygame.time.Clock()
    background = pygame.image.load('assets/bg.jpg')

    mainLoop = True
    while mainLoop:
        screen.blit(background, (0, 0))
        # update screen
        pygame.display.flip()
        
        for event in pygame.event.get():
            # Quit game
            if event.type == pygame.QUIT:
                mainLoop = False
    
    pygame.quit()
    sys.exit()

