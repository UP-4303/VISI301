from classes.StaticObject import StaticObject

from classes.Position import Position

class BlocObject(StaticObject):
    def __init__(self, name:str="Bloc", description:str="Just a massive bloc. You can't go through it.", imageLink:str="./assets/carreblanc.png", healthPoints:int=0, position:Position=Position(0,0)):
        super().__init__(name, description, imageLink, healthPoints, position)