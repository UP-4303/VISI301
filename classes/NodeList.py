from classes.Board import Board
from classes.Node import Node
from classes.Position import Position
from classes.Vector import Vector

# Contains all nodes for pathfinding
class NodeList():
    def __init__(self, board:Board, targets:list, uncrossableTypes:list, objectCoordinates:Position):
        self.size = board.size
        # This list contains all explorable nodes
        self.toExplore = []
        self.targets = targets
        # Create the node list
        self.all = [[Node(Position(x,y), type(board.get(Position(x,y))) in uncrossableTypes, objectCoordinates == Position(x,y), self.HeuristicCost(Position(x,y))) for x in range(board.size[0])] for y in range(board.size[1])]

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
        nodeBottom = self.get(node.coordinates + Vector(-1,0))
        if node.coordinates.x > 0 and not(nodeBottom.uncrossable) and not(nodeBottom.explored):
            # If everything is ok, update it and add it to the toExplore list
            nodeBottom.Update(node.gCost + 1, node)
            self.AddToExplore(nodeBottom)
        nodeTop = self.get(node.coordinates + Vector(1,0))
        if node.coordinates.x < self.size[0] and not(nodeTop.uncrossable) and not(nodeTop.explored):
            nodeTop.Update(node.gCost + 1, node)
            self.AddToExplore(nodeTop)
        nodeLeft = self.get(node.coordinates + Vector(0,-1))
        if node.coordinates.y > 0 and not(nodeLeft.uncrossable) and not(nodeLeft.explored):
            nodeLeft.Update(node.gCost + 1, node)
            self.AddToExplore(nodeLeft)
        nodeRight = self.get(node.coordinates + Vector(0,1))
        if node.coordinates.y < self.size[1] and not(nodeRight.uncrossable) and not(nodeRight.explored):
            nodeRight.Update(node.gCost + 1, node)
            self.AddToExplore(nodeRight)