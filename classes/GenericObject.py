from classes.Position import Position

# This is the default class for an element of the object layer.
class GenericObject():
    name:str
    description:str
    imageLink:str

    healthPoints:int

    position:Position

    def __init__(self, name:str="Generic", description:str="Lorem Ipsum", imageLink:str="NYI", healthPoints:int=0, position:Position=Position(0,0)):
        self.name = name
        self.description = description
        self.imageLink = imageLink
        self.healthPoints = healthPoints
    
    def IsDead(self):
        return self.healthPoints <= 0

    def __repr__(self):
        return self.name