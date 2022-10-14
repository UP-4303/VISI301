from classes.Position import Position
from classes.Floor import Floor

def Pathfinder(actualPosition:Position, targetPosition:Position, floor:Floor):
    path:list[Position] = []
    nodes:list[list[Node]] = [[Node(x,y,actualPosition) for y in range(floor.size.height)] for x in range(floor.size.width)]
    nodesToExplore: list[Node] = [nodes[actualPosition.x][actualPosition.y]]
    return path

class Node(Position):
    hCost: int
    gCost: int
    explored: bool = False

    def __init__(self, x:int, y:int, startingPosition:Position):
        super().__init__(x,y)
        self.hCost = abs(startingPosition - self)
    
    def Explore(self, gCost:int):
        if self.explored:
            if gCost < self.gCost:
                self.gCost = gCost
        else:
            self.gCost = gCost
            self.explored = True