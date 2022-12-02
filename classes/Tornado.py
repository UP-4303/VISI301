import pygame;
from classes.Floor import Floor
from classes.Position import Position
from classes.Event import Event
from classes.Size import Size

class Tornado(Event):
    def __init__(self):
        super().__init__("Tornado", "Hurts on an eneven diagonal", "./assets/tornado.png", 5, Position(0,0) )

    #Make his action on the floor
    def appendOnTheFloor(self,floor: Floor):
       for i in range(0, floor.size.width):
        for j in range(0, floor.size.height):
            if (i==j or ((i-j) <2 and (i-j) >-2)):
                static_objet = floor.getStaticObjects(Position(i,j))
                object_ = floor.GetObject(Position(i,j ))
                if (not(static_objet == None)):
                    static_objet.TakeDamage(1)
                if (not (object_ == None)):
                    object_.TakeDamage(1)


