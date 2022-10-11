
import pygame
from classes.Player import Player


from classes.Floor import Floor
class Game:
    isplaying:bool
    floorList:list[Floor]
    currentFloor:int

    def __init__(self, floorList:list[Floor]=[],currentFloor=0):
        # define is the game has begin
        self.isplaying = True
        self.floorList = floorList
        self.currentFloor = currentFloor





