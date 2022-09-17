class Vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __abs__(self):
        return abs(self.x) + abs(self.y)