class Vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __abs__(self):
        return abs(self.x) + abs(self.y)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)