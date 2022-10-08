import pygame
import sys

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    mainLoop = True
    while mainLoop:
        for event in pygame.event.get():
            # Quit game
            if event.type == pygame.QUIT:
                mainLoop = False
    
    pygame.quit()
    sys.exit()