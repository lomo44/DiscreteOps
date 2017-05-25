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
        self.parent = None
        self.constrain = {}
        self.tempResult = None
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

    def getMaxDegree(self):
        max_degree = -1
        for nodes_index in self.nodes:
            temp_degree = self.nodes[nodes_index].getDegree()
            if temp_degree > max_degree:
                max_degree = temp_degree
        return max_degree



    def testColorable(self, numOfColor):
        def get_color_used(result_list):
            currentMax = -1
            for item in result_list:
                if item != '':
                    if int(item) > currentMax:
                        currentMax = int(item)
            return currentMax+1
        def get_correct_output(result_str, node_list):
            output = [0] * len(node_list)
            counter = 0
            for item in result_str:
                output[node_list[counter].index] = item
                counter+=1
            output_str = ""
            for item in output:
                output_str += str(item) + " "
            return output_str
        def check_feasible_2(s_index, color, result_list):
            for item in sorted_nodes[s_index].neighborsNode:
                s_n_index = mapping_dict[item]
                used_color = int(result_list[s_n_index])
                if used_color == color:
                    return False
            return True
        def detokenize_result(result_str):
            value_list = []
            for item in result_str.split():
                if item != "":
                    value_list.append(int(item))
            return value_list
        def check_is_dead_2(s_index, result_list, target):
            return_str = ""
            constrain_dict = {}
            for index in range(s_index, len(sorted_nodes)):
                banned_color = []
                for n_node in sorted_nodes[index].neighborsNode:
                    s_n_index = mapping_dict[n_node]
                    used_color = int(result_list[s_n_index])
                    if used_color not in banned_color and used_color >= 0:
                        banned_color.append(used_color)
                if len(banned_color) >= target:
                    return True,None
                else:
                    constrain_dict[index] = banned_color
            thingsChanged = True
            while thingsChanged:
                thingsChanged = False
                for each_constrain in constrain_dict:
                    if result_list[each_constrain] == -1:
                        if target - len(constrain_dict[each_constrain]) == 1:
                            for possible_color in range(target):
                                if possible_color not in constrain_dict[each_constrain]:
                                    result_list[each_constrain] = possible_color
                                    thingsChanged = True
                                    for n_node in sorted_nodes[each_constrain].neighborsNode:
                                        s_n_index = mapping_dict[n_node]
                                        if s_n_index in constrain_dict and possible_color not in constrain_dict[s_n_index]:
                                            constrain_dict[s_n_index].append(possible_color)
                                            if target == len(constrain_dict[s_n_index]) and result_list[s_n_index] == -1:
                                                return True,None
                        if target == len(constrain_dict[each_constrain]):
                            return True,None
            for each_constrain in constrain_dict:
                if len(constrain_dict[each_constrain]) >= target:
                    return True,None
                else:
                    return_str += str(each_constrain) + "=" + str(len(constrain_dict[each_constrain]))
            return False,return_str


        temp_solution = []
        start_time = time.time()
        threshold = 10
        max_depth = -1
        target_color = numOfColor
        max_color = sys.maxsize
        global_context_dict = {}

        nodeQueue = []
        rootNode = NodeT()
        rootNode.tempResult = [-1]*len(self.nodes)
        rootNode.depth = 0
        heapq.heappush(nodeQueue, rootNode)

        sorted_nodes = []
        for item in self.nodes:
            sorted_nodes.append(self.nodes[item])

        sorted_nodes.sort(key=lambda x:len(x.neighborsNode), reverse=True)
        mapping_dict = {}
        for node_index in range(len(sorted_nodes)):
            mapping_dict[sorted_nodes[node_index].index] = node_index
        while len(nodeQueue) != 0 and (time.time() - start_time) <= threshold:
            currentNode = heapq.heappop(nodeQueue)
            if(currentNode.depth > max_depth):
                max_depth = currentNode.depth
                print("Depth: ", max_depth)
            current_used_node = get_color_used(currentNode.tempResult)
            if current_used_node <= target_color:
                if -1 in currentNode.tempResult:
                    for color in range(target_color):
                        if check_feasible_2(currentNode.depth, color, currentNode.tempResult):
                            currentNode.tempResult[currentNode.depth] = color
                            deadend,retstr = check_is_dead_2(currentNode.depth+1,currentNode.tempResult,target_color)
                            if not deadend:
                                if currentNode.depth not in global_context_dict:
                                    global_context_dict[currentNode.depth] = []
                                if retstr not in global_context_dict[currentNode.depth] and currentNode.depth < len(self.nodes):
                                    # branch a new tree
                                    global_context_dict[currentNode.depth].append(retstr)
                                    newNode = NodeT()
                                    for result_index in range(len(currentNode.tempResult)):
                                        if currentNode.tempResult[result_index] == -1:
                                            newNode.depth = result_index
                                    newNode.depth = currentNode.depth+1
                                    newNode.tempResult = copy.deepcopy(currentNode.tempResult)
                                    heapq.heappush(nodeQueue,newNode)

                else:
                    currentMax = get_color_used(currentNode.tempResult)
                    if currentMax <= target_color and currentMax < max_color:
                        max_depth = -1
                        max_color = currentMax
                        temp_solution = get_correct_output(currentNode.tempResult, sorted_nodes)
                        target_color -= 1
                        print("{0} color solution found, moving to: {1}".format(max_color, target_color))
        if len(temp_solution) != 0:
            print("{0} color feasible".format(max_color))
        else:
            print("{0} color is not feasible".format(numOfColor))
        return temp_solution

