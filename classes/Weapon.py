from classes.Position import Position

class Weapon():
    pattern:list[list[int]]
    center: Position

    def __init__(self, pattern:list[list[int]]=[[0]], center:Position=Position(0,0)):
        self.pattern = pattern
        self.center = center