from classes.Position import Position
from classes.Vector import Vector

# Search for MOVEMENT target
def TargetStraightLine(object, targetTypes:list, distance:int):
    targets = []
    # For every cell
    for y in range(object.board.size[1]):
        for x in range(object.board.size[0]):
            # If the cell is empty or is the object itself
            if object.board.get(Position(x,y)) == None or object.board.get(Position(x,y)) == object:
                # Check if this cell is a valid target.
                # elif is used instead of if to prevent duplication
                if x-distance >= 0 and type(object.board.get(Position(x-distance,y))) in targetTypes:
                    targets.append(Position(x,y))
                elif x+distance < object.board.size[0] and type(object.board.get(Position(x+distance,y))) in targetTypes:
                    targets.append(Position(x,y))
                elif y-distance >= 0 and type(object.board.get(Position(x,y-distance))) in targetTypes:
                    targets.append(Position(x,y))
                elif y+distance < object.board.size[1] and type(object.board.get(Position(x,y+distance))) in targetTypes:

                    targets.append(Position(x,y))
    return targets

# HTH stands for Hand-To-Hand. If true, it will hit the cell next to it. If false, it will hit the first non-empty cell in the line
# Direction is a normalized vector
def HitStraightLine(object, direction:Vector, HTH:bool, damages:int):
    if (object.coordinates + direction).InBoard(object.board.size):
        target = object.board.get(object.coordinates + direction)
        if HTH:
            if target != None:
                target.TakeDamage(damages)
        else:
            distance = 1
            target = object.board.get(object.coordinates + direction)
            while (object.coordinates + (direction*(distance+1))).InBoard(object.board.size) and target == None:
                distance += 1
                target = object.board.get(object.coordinates + (direction*distance))
            if target != None:
                target.TakeDamage(damages)