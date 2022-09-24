from classes.Position import Position

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