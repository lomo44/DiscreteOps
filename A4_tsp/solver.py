#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from collections import namedtuple
import networkx as nx
import matplotlib.pyplot as plt
import time

Point = namedtuple("Point", ['x', 'y'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def parse_data(input_data):
    lines = input_data.split('\n')

    nodeCount = int(lines[0])

    points = []
    for i in range(1, nodeCount + 1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))
    return points

def plot_result(solution, pointlist):
    G = nx.Graph()
    for item in pointlist:
        G.add_node(item, pos=pointlist[item])
    for index in range(0, len(solution)-1):
        G.add_edge(solution[index],solution[index+1])
    G.add_edge(solution[0], solution[len(solution)-1])
    pos = nx.get_node_attributes(G, 'pos')
    # generate solution label
    label = {}
    for item in solution:
        label[item] = item

    nx.draw(G, pos)

    # plt.ion()
    # plt.draw()
    # plt.pause(3)
    nx.draw_networkx_labels(G, pos, label)
    # plt.draw()
    # plt.pause(3)
    plt.show()
    pass
def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input

    # build a trivial solution
    # visit the nodes in the order they appear in the file
    points = parse_data(input_data)
    point_dict = {}
    for index in range(len(points)):
        point_dict[index] = points[index]
    solution = range(0, len(points))

    # calculate the length of the tour
    obj = length(points[solution[-1]], points[solution[0]])
    for index in range(0, len(points)-1):
        obj += length(points[solution[index]], points[solution[index+1]])


    plot_result(solution, point_dict)

    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))
    return output_data


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')

