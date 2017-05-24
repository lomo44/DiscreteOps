import heapq
import sys
import copy
import time
class Node:
    def __init__(self):
        self.index = -1
        self.neighborsNode = {}
        self.status = 0 #0 unvisited 1 will visit 2 visited
        self.depth = -1
        self.BannedColor = []
        self.appliedContrain = []
        self.color = -1
    def __eq__(self, other):
        return self.index == other.index

    def __lt__(self, other):
        return self.index < other.index

    def getDegree(self):
        return len(self.neighborsNode)
class NodeT:
    def __init__(self):
        self.depth = 0
        self.childs = []
        self.parent = None
        self.constrain = {}
        self.tempResult = ""
    def __lt__(self, other):
        return self.depth > other.depth



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

    def testColorable(self, numOfColor):
        def populate_constrain(constrain_list, constrain_dict):
            constrain_added = []
            for constrain in constrain_list:
                if constrain[0] not in constrain_dict:
                    constrain_dict[constrain[0]] = []
                if constrain[1] not in constrain_dict[constrain[0]]:
                    constrain_dict[constrain[0]].append(constrain[1])
                    constrain_added.append(constrain)
            return constrain_added
        def unpopulate_constrain(constrain_list, constrain_dict):

            for constrain in constrain_list:
                if constrain[0] in constrain_dict:
                    if constrain[1] in constrain_dict[constrain[0]]:
                        constrain_dict[constrain[0]].remove(constrain[1])


        def get_context_str(constrain_dict):
            output_str = ""
            for item in sorted(constrain_dict.keys()):
                output_str += str(item) + "-" + str(len(constrain_dict[item])) + ','
            return output_str

        def check_feasible(node_index, color, constrain_dict):
            if node_index in constrain_dict:
                if color in constrain_dict[node_index]:
                    return False
                return True
            else:
                return True
        def get_color_used(result_str):
            results = result_str.split(" ")
            currentMax = -1
            for item in results:
                if item != '':
                    if int(item) > currentMax:
                        currentMax = int(item)
            return currentMax+1
        nodeQueue = []
        rootNode = NodeT()
        rootNode.depth = 0
        heapq.heappush(nodeQueue,rootNode)
        max_color = sys.maxsize
        temp_solution = []
        start_time = time.time()
        threshold = 300
        max_depth = -1
        while len(nodeQueue) != 0 and (time.time() - start_time) <= threshold:
            #print("Node Count: ", len(nodeQueue))
            currentNode = heapq.heappop(nodeQueue)
            if(currentNode.depth > max_depth):
                max_depth = currentNode.depth
                print("Depth: ", max_depth)
            current_used_node = get_color_used(currentNode.tempResult)
            if current_used_node < max_color:
                if currentNode.depth < len(self.nodes):
                    hasColor = False
                    context_str_list = []
                    for color in range(numOfColor):
                        if check_feasible(currentNode.depth, color, currentNode.constrain):
                            hasColor = True
                            next_constrain = []
                            # start expanding the tree
                            for neightbor_index in self.nodes[currentNode.depth].neighborsNode:
                                next_constrain.append((neightbor_index,color))
                            constrain_added = populate_constrain(next_constrain, currentNode.constrain)
                            deadend = False
                            for eachConstrain in currentNode.constrain:
                                if len(currentNode.constrain[eachConstrain]) >= numOfColor:
                                    deadend = True
                                    break
                            if not deadend:
                                this_context_str = get_context_str(currentNode.constrain)
                                if this_context_str not in context_str_list and currentNode.depth < len(self.nodes):
                                    # branch a new tree
                                    context_str_list.append(this_context_str)
                                    newNode = NodeT()
                                    newNode.depth = currentNode.depth+1
                                    newNode.constrain = copy.deepcopy(currentNode.constrain)
                                    newNode.tempResult = currentNode.tempResult + str(color) + " "
                                    heapq.heappush(nodeQueue,newNode)
                            unpopulate_constrain(constrain_added, currentNode.constrain)
                else:
                    currentMax = get_color_used(currentNode.tempResult)
                    if currentMax < max_color:
                        max_color = currentMax
                        print("Aha", max_color)
                        temp_solution = currentNode.tempResult
        if len(temp_solution) != 0:
            print("{0} color feasible".format(max_color))
        else:
            print("{0} color is not feasible".format(numOfColor))
        return temp_solution
    def getMaxDegree(self):
        max_degree = -1
        for nodes_index in self.nodes:
            temp_degree =self.nodes[nodes_index].getDegree()
            if temp_degree > max_degree:
                max_degree = temp_degree
        return max_degree