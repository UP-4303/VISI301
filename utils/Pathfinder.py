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
    nodeList = NodeList(board, uncrossableTypes, object.coordinates)
    nodeList.all[object.coordinates.y][object.coordinates.x].Update(0, object.coordinates)
    nodeList.AddToExplore(nodeList.get(object.coordinates))

    currentNode = nodeList.Explore()
    while not(currentNode in targets) and len(nodeList.toExplore) > 0:
        currentNode = nodeList.Explore()
    if currentNode in targets:
        path = Path(nodeList, currentNode)