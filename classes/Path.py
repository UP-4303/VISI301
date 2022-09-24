from classes.Node import Node

class Path():
    def __init__(self, endNode:Node):
        self.value = []
        node = endNode
        while not(node.start):
            self.value.insert(0, node)
            node = node.pointToNode
        self.value.insert(0, node)