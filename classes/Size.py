from typing import Any

class Size():
    width:int # Width is x
    height:int  # Height is y

    def __init__(self, width:int, height:int):
        self.width = width
        self.height = height
        if self.width < 0 or self.height < 0:
            raise ValueError(f"{self} width and height must be positive : {self.__repr__}")

    def __eq__(self, other:Any):
        if isinstance(other, self.__class__):
            return self.width == other.width and self.height == other.height
        else:
            return False

    def __ne__(self, other:Any):
        return not self.__eq__(other)

    def __repr__(self):
        return f'Size(width={self.width}, height={self.height})'