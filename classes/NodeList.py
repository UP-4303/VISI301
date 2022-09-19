from classes.Node import Node

class NodeList():
    def __init__(self,size):
        self.all = [[Node for x in range(size[0])] for y in range(size[1])]
