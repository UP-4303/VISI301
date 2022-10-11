from classes.GenericObject import GenericObject

from classes.Position import Position

# This is the subclass for objects that can't move.
class StaticObject(GenericObject):
    def __init__(self, name:str="Static", description:str="Lorem Ipsum", imageLink:str="./assets/carreblanc.png", healthPoints:int=0, position:Position=Position(0,0)):
        super().__init__(name, description, imageLink, healthPoints, position)