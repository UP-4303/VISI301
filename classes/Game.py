
import pygame
from classes.Player import Player
from classes.Monster import Monster

from classes.Floor import Floor
class Game:
    score: int
    isplaying:bool
    floorList:list[Floor]
    currentFloor:int

    def __init__(self, floorList:list[Floor]=[],currentFloor=0):
        # define is the game has begin
        self.isplaying = True
        self.floorList = floorList
        self.currentFloor = currentFloor
        self.score = 0
        #generate the player
        self.player = Player()
        self.list_player = pygame.sprite.Group()
        #keep all the monsters in a groupe
        self.all_monsters = pygame.sprite.Group()

        #TEST A ENLEVER
        self.spawn_monster()




    def update(self, screen):
        # show the score on the screen

        font = pygame.font.SysFont("monospace", 25, True) #create the font style
        score_text = font.render("Score :" + str(self.score),1, (255,255,255))  #create texte
        screen.blit(score_text, (640,60)) #show the score at the tuple position

        # show monstres (maybe better in main)
        self.all_monsters.draw(screen)

        # show the player
        self.list_player.draw(screen)



    #Generate a monster
    def spawn_monster(self):
        monster = Monster()
        self.all_monsters.add(monster)

