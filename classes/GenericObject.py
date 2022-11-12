import pygame

from classes.Position import Position

# This is the default class for an element of the object layer.
class GenericObject(pygame.sprite.Sprite):
    name:str
    description:str
    imageLink:str
    healthPoints:int
    maxHealthPoints:int
    position:Position

    def __init__(self, name:str="Generic", description:str="Lorem Ipsum", imageLink:str="./assets/carreblanc.png", healthPoints:int=0, position:Position=Position(0,0)):
        super().__init__()
        self.name = name
        self.description = description
        self.imageLink = imageLink
        self.healthPoints = healthPoints
        self.maxHealthPoints = healthPoints

        self.image = pygame.image.load(self.imageLink)
        self.rect = self.image.get_rect()
        self.position = position

    # indicate by a boolean if the Object is dead
    def IsDead(self):
        return self.healthPoints <= 0

    # The object loose the number of life points indicated.
    def TakeDamage(self, damage:int):
        self.healthPoints = max ((self.healthPoints - damage), 0)

    # The object gain the number of life points indicated.
    def RecoverHealth(self, recover:int):
        self.healthPoints = min(self.healthPoints + recover, self.maxHealthPoints)


    def __repr__(self):
        return self.name

    # Utile : nous pouvons créer des groupes avec pygame.sprite.Group()
    # all_player.add(player)
    # all_player.draw(screen)
    # for player in all_player :
    # self.all_players.remove(self)

    # Pour redimentioner une image
    # self.image = pygame.transform.scale (self.image, (50, 50))
