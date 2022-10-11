import pygame

from classes.Position import Position

# This is the default class for an element of the object layer.
class GenericObject(pygame.sprite.Sprite):
    name:str
    description:str
    imageLink:str

    healthPoints:int
    maxhealthPoints:int

    position:Position

    def __init__(self, name:str="Generic", description:str="Lorem Ipsum", imageLink:str="./assets/carreblanc.png", healthPoints:int=0, position:Position=Position(0,0)):
        super().__init__()
        self.name = name
        self.description = description
        self.imageLink = imageLink
        self.healthPoints = healthPoints
        self.maxhealthPoints = healthPoints

        self.image = pygame.image.load(self.imageLink)
        self.rect = self.image.get_rect()
    
    def IsDead(self):
        return self.healthPoints <= 0

    def __repr__(self):
        return self.name