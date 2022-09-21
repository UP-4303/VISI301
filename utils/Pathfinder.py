from math import inf

from classes.Board import Board
from classes.Bloc import Bloc
from classes.Node import Node
from classes.NodeList import NodeList
from classes.Path import Path
from classes.Player import Player
from classes.Position import Position
from classes.Vector import Vector

# For the pathfinder, we will use an adapted A* algorithm for cardinal neighborhood
# This function return a path object (which is a list of positions)
def Pathfinder(board:Board, object, targets:list, uncrossableTypes:list):
    nodeList = NodeList(board, targets, uncrossableTypes, object.coordinates)
    nodeList.get(object.coordinates).Update(0, nodeList.get(object.coordinates))

    for i in targets:
        print(i.x, i.y)

    currentNode = nodeList.Explore()
    while not(currentNode.coordinates in targets) and len(nodeList.toExplore) > 0:
        currentNode = nodeList.Explore()

    if currentNode.coordinates in targets:
        path = Path(currentNode)
    else:
        path = Path(nodeList.get(object.coordinates))
    return path