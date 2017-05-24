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

    def getMaxDegree(self):
        max_degree = -1
        for nodes_index in self.nodes:
            temp_degree = self.nodes[nodes_index].getDegree()
            if temp_degree > max_degree:
                max_degree = temp_degree
        return max_degree



    def testColorable(self, numOfColor):
        def populate_constrain(constrain_list, constrain_dict, current_node_depth):
            constrain_added = []
            for constrain in constrain_list:
                if constrain[0] > current_node_depth:
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
        def get_context_str(constrain_dict, current_node_index):
            output_str = ""
            for item in sorted(constrain_dict.keys()):
                if item > current_node_index:
                    output_str += str(item) + "-" + str(len(constrain_dict[item])) + ','
            return output_str
        def check_feasible(node_index, color, constrain_dict):
            if node_index in constrain_dict:
                if color in constrain_dict[node_index]:
                    return False
                return True
            else:
                return True
        def check_is_dead(constrain_dict, node_depth, target):
            for eachConstrain in constrain_dict:
                if eachConstrain > node_depth:
                    if len(constrain_dict[eachConstrain]) >= target:
                        return True
            return False
        def get_color_used(result_str):
            results = result_str.split(" ")
            currentMax = -1
            for item in results:
                if item != '':
                    if int(item) > currentMax:
                        currentMax = int(item)
            return currentMax+1
        def get_next_constrain(constrain_dict, node_depth):
            ret = {}
            for each_node in constrain_dict:
                if each_node > node_depth:
                    ret[each_node] = copy.deepcopy(constrain_dict[each_node])
            return ret
        def build_constrain_dict(result_str, node_list):
            return_dict = {}
            results = result_str.split(" ")
            for index in range(len(results)):
                if results[index] != "":
                    for node in node_list[index].neighborsNode:
                        if node not in return_dict:
                            return_dict[node] = []
                        if int(results[index]) not in return_dict[node]:
                            return_dict[node].append(int(results[index]))
            return return_dict
        def get_correct_output(result_str, node_list):
            output = [0] * len(node_list)
            counter = 0
            for item in result_str.split(" "):
                if item != "":
                    output[node_list[counter].index] = item
                counter+=1
            output_str = ""
            for item in output:
                output_str += str(item) + " "
            return output_str
        def check_feasible_2(s_index, color, result_list):
            banned_color = []
            for item in sorted_nodes[s_index].neighborsNode:
                s_n_index = mapping_dict[item]
                if s_n_index < len(result_list):
                    used_color = int(result_list[s_n_index])
                    if used_color not in banned_color:
                        banned_color.append(used_color)
            if color not in banned_color:
                return True
            else:
                return False
        def detokenize_result(result_str):
            value_list = []
            for item in result_str.split():
                if item != "":
                    value_list.append(int(item))
            return value_list
        def check_is_dead_2(s_index, result_list, target):
            return_str = ""
            for index in range(s_index, len(sorted_nodes)):
                banned_color = []
                for n_node in sorted_nodes[index].neighborsNode:
                    s_n_index = mapping_dict[n_node]
                    if s_n_index < len(result_list):
                        used_color = int(result_list[s_n_index])
                        if used_color not in banned_color:
                            banned_color.append(used_color)
                if len(banned_color) >= target:
                    return True,None
                else:
                    return_str += str(index) + "=" + str(len(banned_color)) + ","
            return False,return_str

        nodeQueue = []
        rootNode = NodeT()
        rootNode.depth = 0
        heapq.heappush(nodeQueue,rootNode)
        max_color = sys.maxsize
        temp_solution = []
        start_time = time.time()
        threshold = 300
        max_depth = -1
        target_color = numOfColor
        global_context_dict = {}

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
            if current_used_node < max_color:
                if currentNode.depth < len(self.nodes):
                    current_result = detokenize_result(currentNode.tempResult)
                    for color in range(target_color):
                        if check_feasible_2(currentNode.depth, color, current_result):
                            potential_result = currentNode.tempResult + str(color) + " "
                            potential_result_2 = current_result + [color]
                            deadend,retstr = check_is_dead_2(currentNode.depth+1,potential_result_2,target_color)
                            if not deadend:
                                if currentNode.depth not in global_context_dict:
                                    global_context_dict[currentNode.depth] = []
                                if retstr not in global_context_dict[currentNode.depth] and currentNode.depth < len(self.nodes):
                                    # branch a new tree
                                    global_context_dict[currentNode.depth].append(retstr)
                                    newNode = NodeT()
                                    newNode.depth = currentNode.depth+1
                                    newNode.tempResult = potential_result
                                    heapq.heappush(nodeQueue,newNode)

                else:
                    currentMax = get_color_used(currentNode.tempResult)
                    if currentMax < max_color:
                        max_depth = -1
                        max_color = currentMax
                        temp_solution = get_correct_output(currentNode.tempResult, sorted_nodes)
                        target_color-=1
                        print("{0} color solution found, moving to: {1}".format(max_color, target_color))
            else:
                print("Color prune")
        if len(temp_solution) != 0:
            print("{0} color feasible".format(max_color))
        else:
            print("{0} color is not feasible".format(numOfColor))
        return temp_solution

