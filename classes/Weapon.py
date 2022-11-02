import pygame
from classes.Position import Position

class Weapon(pygame.sprite.Sprite):
    pattern:list[list[int]]
    center: Position
    imageLink: str

    def __init__(self, pattern:list[list[int]]=[[0]], center:Position=Position(0,0), imageLink:str="./assets/weapon1.png"):
        self.pattern = pattern
        self.center = center
        self.imageLink = imageLink

