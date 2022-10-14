
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
        self.player = Player()

    def update(self, screen):
        # show the score on the screen
        font = pygame.font.SysFont("monospace", 16) #create the font style
        score_text = font.render("Score :" + str(self.score),1, (255,0,0))  #create texte
        screen.blit(score_text, (20,20)) #show the score at the tuple position

        # show monstres





