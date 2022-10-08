import pygame

pygame.init()

#Generate the window of the game

pygame.display.set_caption("Our game")
screen = pygame.display.set_mode((1080,720)) # define the dimention of the window

#import background
background = pygame.image.load('assets/bg.jpg')


running = True #indicate  if the game is running

# game loop wich repeats utile running is false

while running :
    #apply background
    screen.blit(background, (0, 0))

    # update screen
    pygame.display.flip()


    #Loop that will treat one by one ech event on the event list

    for event in pygame.event.get():
        # Dealing with closing
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("Game has been closed")

