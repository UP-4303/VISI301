import pygame
from classes.game import Game
from classes.player_first import Player

pygame.init()

#Generate the window of the game

pygame.display.set_caption("Our game")
screen = pygame.display.set_mode((1080,720)) # define the dimention of the window

#import background
background = pygame.image.load('assets/bg.jpg')

#download the game
game= Game()

#init player
player = Player()

running = True #indicate  if the game is running

# game loop wich repeats utile running is false

while running :
    # apply background
    screen.blit(background, (0, 0))

    # chech if the game has started
    #if game.isplaying:

        # apply joueur
        #screen.blit(self.player.image, player.rect)

        # Loop that will treat one by one ech event on the event list

    for event in pygame.event.get():
        # Dealing with closing
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("Game has been closed")

        # detect if player has touched a key on the keyboard
        elif event.type == pygame.KEYDOWN:
            # wich one
            if event.key == pygame.K_q:
                print("you touched q")
            elif event.key == pygame.K_RETURN:
                print("you touched return")
    # update screen
    #pygame.display.flip()



