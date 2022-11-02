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

    # import welcome background
    banner = pygame.image.load('assets/banner.png')
    banner = pygame.transform.scale(banner, (700,700))
    banner_rect = banner.get_rect()
    banner_rect.x = (screen.get_width() // 2) - (banner.get_width() //2)

    # import button to start the game
    play_button = pygame.image.load('assets/button_play.png')
    play_button = pygame.transform.scale(play_button, (400,150))
    play_button_rect = play_button.get_rect()
    play_button_rect.x = (screen.get_width() // 2) - (play_button.get_width() //2)
    play_button_rect.y = (screen.get_height()) - (play_button.get_height() +22)

    running = True #indicate  if the game is running

    while running:
        #apply the window of the game
        screen.blit(background, (0, 0))

        # check if the game has started
        if game.isplaying:
            #launch the game instruction
            running = game.update(screen)
        # check if the game has not started yet
        else:
            #add the welcoming screen
            screen.blit(banner, banner_rect)
            screen.blit(play_button, play_button_rect)

        # deal with quitting or beginning the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                # check if the mouse collide the button play
                if play_button_rect.collidepoint(event.pos):
                    game.isplaying = True

        # update screen
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

