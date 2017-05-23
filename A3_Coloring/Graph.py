import heapq

class Node:
    def __init__(self):
        self.index = -1
        self.neighborsNode = {}
        self.status = 0 #0 unvisited 1 will visit 2 visited
        self.depth = -1
        self.BannedColor = []
        self.color = -1

    def __eq__(self, other):
        return self.index == other.index

    def __lt__(self, other):
        return self.index < other.index

class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = []

    def expand(self,edge_list):
        self.edges = edge_list
        for edge in self.edges:
            for vertex in edge:
                if vertex not in self.nodes:
                    self.nodes[vertex] = Node()
                    self.nodes[vertex].index = vertex
            if edge[1] not in self.nodes[edge[0]].neighborsNode:
                self.nodes[edge[0]].neighborsNode[edge[1]] = self.nodes[edge[1]]
            if edge[0] not in self.nodes[edge[1]].neighborsNode:
                self.nodes[edge[1]].neighborsNode[edge[0]] = self.nodes[edge[0]]

