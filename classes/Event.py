import pygame;
from classes.Floor import Floor
from classes.Position import Position

class Event(pygame.sprite.Sprite):
    def __init__(self, name:str="Evenement",  description:str="This is an event", imageLink:str="./assets/carreblanc.png", price:int=0 , position:Position=Position(0,0)):
        super().__init__()
        self.name = name;
        self.description= description;
        self.imageLink = imageLink;
        self.price = price;
        self.positionToAttack = Position(0,0);

        self.image = pygame.image.load(self.imageLink)
        self.rect = self.image.get_rect()

        #Make his action on the floor
        def appendOnTheFloor(self,floor: Floor):
            pass;


