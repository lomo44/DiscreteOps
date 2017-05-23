#!/usr/bin/python
# -*- coding: utf-8 -*-
from A3_Coloring.Graph import *
import heapq

def parseEdge(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))
    return node_count,edge_count,edges

def mark1(edges):
    newGraph = Graph()
    newGraph.expand(edges)
    # very naive solution

    used_index = {}
    usable_index = {}
    for index in range(len(newGraph.nodes)):
        used_index[index] = False
        usable_index[index] = True

    nodeQueue = []
    for node_index in newGraph.nodes:
        nodeQueue.append(newGraph.nodes[node_index])
    nodeQueue.sort(key=lambda x:len(x.neighborsNode), reverse=True)
    for item in nodeQueue:
        item.status = 2
        # banned color
        for color in item.BannedColor:
            usable_index[color] = False
        print(item.BannedColor)
        # looking for a possible color
        usable_color = -1
        for color in usable_index:
            if usable_index[color]:
                usable_color = color
                break
        # unbaneed color
        for color in item.BannedColor:
            usable_index[color] = True
        # mark used color
        if used_index[usable_color] is False:
            used_index[usable_color] = True
        # assign color
        item.color = usable_color
        # print("Node Index: {0}, color: {1}".format(node.index,usable_color))
        # propagate constrain
        for node_index in item.neighborsNode:
            if item.neighborsNode[node_index].status < 2:
                if usable_color not in item.neighborsNode[node_index].BannedColor:
                    item.neighborsNode[node_index].BannedColor.append(usable_color)

    output_data = str(len(newGraph.nodes)) + ' ' + str(0) + '\n'
    max_value = 0
    for item in sorted(newGraph.nodes.keys()):
        if newGraph.nodes[item].color > max_value:
            max_value = newGraph.nodes[item].color
        output_data += str(newGraph.nodes[item].color)+" "
    print("Color Count: ", max_value)
    return output_data

def solve_it(input_data):

    node_count,edge_count,edges = parseEdge(input_data)    # Modify this code to run your optimization algorithm
    # # every node has its own color
    # solution = range(0, node_count)
    #
    # # prepare the solution in the specified output format
    # output_data = str(node_count) + ' ' + str(0) + '\n'
    # output_data += ' '.join(map(str, solution))

    return mark1(edges)


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

