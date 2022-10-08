from classes.GenericObject import GenericObject

from classes.Position import Position

# This is a subclass of GenericObject for objects that can move.
class MoveableObject(GenericObject):
    movementPoints:int

    def __init__(self, name:str="Moveable", description:str="Lorem Ipsum", imageLink:str="NYI", healthPoints:int=0, position:Position=Position(0,0), movementPoints:int=0):
        super().__init__(name, description, imageLink, healthPoints, position)
        self.movementPoints = movementPoints