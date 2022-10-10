import pygame
import sys

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