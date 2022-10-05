from classes.Board import Board
from classes.Node import Node
from classes.Position import Position
from classes.Vector import Vector

# Contains all nodes for pathfinding
class NodeList():
    def __init__(self, board:Board, targets:list, uncrossableTypes:list, objectCoordinates:Position):
        self.size = board.size
        self.targets = targets
        # Create the node list
        self.all = [[Node(Position(x,y), type(board.get(Position(x,y))) in uncrossableTypes, Position(x,y) == objectCoordinates, hCost=self.HeuristicCost(Position(x,y))) for x in range(self.size[0])] for y in range(self.size[1])]
        # This list contains all explorable nodes
        self.toExplore = [self.get(objectCoordinates)]
        

    # Calculate distance to nearest target
    def HeuristicCost(self, position:Position):
        hCosts = []
        for target in self.targets:
            hCosts.append(abs(target - position))
        return min(hCosts)
    
    # Get the node in coordinates
    def get(self, coordinates:Position):
        return self.all[coordinates.y][coordinates.x]
    
    # Set the node in coordinates to newValue
    def set(self, coordinates:Position, newValue:Node):
        self.all[coordinates.y][coordinates.x] = newValue

    # This node can be explored
    def AddToExplore(self, node:Node):
        self.toExplore.append(node)
    
    # Return the next node to explore
    def NextNode(self):
        nextNode = self.toExplore[0]
        for node in self.toExplore[1:]:
            # If total cost is lower or equal and heuristic cost is lower, this node will be explored before
            if node.Cost() < nextNode.Cost() or node.Cost() == nextNode.Cost() and node.hCost < nextNode.hCost:
                nextNode = node
        self.toExplore.remove(nextNode)
        return nextNode
    
    # Request a node to explore and add new nodes to the toExplore list
    def Explore(self):
        node = self.NextNode()
        node.Explore()

        # For each adjacent node, check if it exist and if it is crossable and if it is unexplored
        if node.coordinates.x > 0:
            nodeBottom = self.get(node.coordinates + Vector(-1,0))
            if not(nodeBottom.uncrossable) and not(nodeBottom.explored):
                # If everything is ok, update it and add it to the toExplore list
                nodeBottom.Update(node.gCost + 1, node)
                if not(nodeBottom in self.toExplore):
                    self.AddToExplore(nodeBottom)
        if node.coordinates.x < self.size[0]-1:
            nodeTop = self.get(node.coordinates + Vector(1,0))
            if not(nodeTop.uncrossable) and not(nodeTop.explored):
                nodeTop.Update(node.gCost + 1, node)
                if not(nodeTop in self.toExplore):
                    self.AddToExplore(nodeTop)
        if node.coordinates.y > 0:
            nodeLeft = self.get(node.coordinates + Vector(0,-1))
            if not(nodeLeft.uncrossable) and not(nodeLeft.explored):
                nodeLeft.Update(node.gCost + 1, node)
                if not(nodeLeft in self.toExplore):
                            self.AddToExplore(nodeLeft)
        if node.coordinates.y < self.size[1]-1:
            nodeRight = self.get(node.coordinates + Vector(0,1))
            if not(nodeRight.uncrossable) and not(nodeRight.explored):
                nodeRight.Update(node.gCost + 1, node)
                if not(nodeRight in self.toExplore):
                    self.AddToExplore(nodeRight)
        return node