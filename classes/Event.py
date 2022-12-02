import pygame;
from classes.Floor import Floor
from classes.Position import Position

class Event():
    def __init__(self, name:str="Evenement",  description:str="This is an event", imageLink:str="./assets/carreblanc.png", price:int=0 , position:Position=Position(0,0)):
        self.name = name;
        self.description= description;
        self.imageLink = imageLink;
        self.price = price;
        self.positionToAttack = Position(0,0);

        #Make his action on the floor
        def appendOnTheFloor(self,floor: Floor):
            pass;


