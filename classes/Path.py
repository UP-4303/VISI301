from classes.Node import Node
from classes.NodeList import NodeList

class Path():
    def __init__(self, nodeList:NodeList, endNode:Node):
        self.value = []
        node = endNode
        while not(node.start):
            self.value.insert(0, node)
            node = node.pointToNode
        self.value.insert(0, node)