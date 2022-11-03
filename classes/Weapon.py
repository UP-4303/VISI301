import pygame
from typing import Any

from classes.Position import Position

class Weapon(pygame.sprite.Sprite):
    name:str
    pattern:dict[str,Any]
    onPick:dict[str,Any]
    onDrop:dict[str,Any]
    onAttack:dict[str,Any]
    imageLink: str

    def __init__(self, name:str='Weapon', imageLink:str='/assets/weapon1.png', **kwargs):
        self.name = name
        self.imageLink = imageLink

        for key,value in kwargs.items():
            setattr(self,key,value)

