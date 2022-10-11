
import pygame
from classes.Player import Player


class Game:
    def __init__(self):
        #genere notre joueur
        self.player = Player();

        #groupes de monstres
        self.all_monsters = pygame.sprite.Group()

        # define is th game has begin
        #self.isplaying = False

    #update all component of the game
    # Recuperer dans le main



