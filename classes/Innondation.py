import pygame;
from classes.Floor import Floor
from classes.Position import Position
from classes.Event import Event
from classes.Size import Size

class Innondation(Event):
    def __init__(self):
        super().__init__("Innondation", "Hurts everything on the border", "./assets/water.png", 10, Position(0,0) )

    #Make his action on the floor
    def appendOnTheFloor(self,floor: Floor):
       for i in range(0, floor.size.width):
        for j in range(0, floor.size.height):
            if (i==0 or j==0 or i==floor.size.width -1 or j == floor.size.height-1):
                static_objet = floor.getStaticObjects(Position(i,j))
                object_ = floor.GetObject(Position(i,j ))
                if (not(static_objet == None)):
                    static_objet.TakeDamage(1)
                if (not (object_ == None)):
                    object_.TakeDamage(1)



