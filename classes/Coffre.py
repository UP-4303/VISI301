import time

from classes.PickableObject import PickableObject
from classes.Player import Player
from classes.OpenableObject import OpenableObject
from classes.Position import Position
from classes.Weapon import Weapon
import pygame

class Coffre(OpenableObject):


    def __init__(self, position:Position=Position(0,0),insideTheBox: list = [] ):
        super().__init__("Coffre", "Box containes weapons or pickable", "./assets/coffre.png", 4, position)
        self.insideTheBox=insideTheBox

    def isOpen(self, Player):
        weapons = []
        for object_ in self.insideTheBox:
            if isinstance(object_, PickableObject):
                object_.ispicked(Player)
            elif isinstance(object_, Weapon):
                weapons += object_
        return weapons

    def showInside(self, screen):

            font_large = pygame.font.SysFont("monospace", 25, True)  # create the font style
            font_small = pygame.font.SysFont("monospace", 10, True)  # create the font style

            x_start = self.rect.x + 20
            y_start = self.rect.y +20
            taille = 60


            # draw the weapons
            taille = 60
            DEFAULT_IMAGE_SIZE = (taille, taille)
            ecart = 0
            compte_arme = 0
            x = x_start
            y = y_start

            for treasure in self.insideTheBox:

                back_square_pos = [x, y-10, taille, taille+20]  # x, y, w, h
                pygame.draw.rect(screen, (187, 174, 152), back_square_pos)

                image_treasure = pygame.image.load(treasure.imageLink)  # import image
                image_treasure = pygame.transform.scale(image_treasure, DEFAULT_IMAGE_SIZE)
                screen.blit(image_treasure, (x, y))

                txt_arme = font_small.render(treasure.name, 1, (255, 255, 255))
                screen.blit(txt_arme, (x, y + taille))

                x = x + ecart + taille















