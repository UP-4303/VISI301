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

    def __init__(self, name:str='Weapon', **kwargs):
        #kwargs is zero, one or infinity of parameters

        self.name = name 
        self.button = pygame.Rect(0,0,0,0)

        for key,value in kwargs.items():
            setattr(self,key,value)
        if getattr(self, 'imageLink', None):
            setattr(self, 'imageLink', '/assets/weapon1.png')

    def Action(self, action:str, wielder:Any):
        actionValue = getattr(self, action, None)
        if actionValue != None:
            for key,value in actionValue.items():
                match key:
                    case "statLifeAdd":
                        if value > 0:
                            wielder.RecoverHealth(value)
                        else:
                            wielder.TakeDamage(value)
                    case "statMaxLifeAdd":
                        wielder.maxHealthPoints += value
                    case "statLifeSet":
                        wielder.healthPoints = value
                    case "statMaxLifeSet":
                        wielder.maxHealthPoints = value
                    case "pattern":
                        pattern = actionValue['pattern']

    def GetAttackPattern(self):
        onAttack = getattr(self, 'onAttack', None)
        if onAttack is None:
            return {}
        else:
            return onAttack.get('pattern', {})

    def __repr__(self):
        representation:str = ""

        for key,value in self.__dict__.items():
            representation += f'{key}:{value} | '
        return representation