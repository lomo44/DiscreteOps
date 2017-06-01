#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from collections import namedtuple
import networkx as nx
import matplotlib.pyplot as plt
from A4_tsp.tsp_util import *
from A4_tsp.tsp_solver import *
import time

Point = namedtuple("Point", ['x', 'y'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)



def plot_result(solution, point_dict):
    G = nx.Graph()
    for item in point_dict:
        G.add_node(item, pos=point_dict[item])
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


    distance_dict = load_distance_dict(str(len(point_dict))+".cache")
    greedy_result, greedy_solution = tsp_master(point_dict,distance_dict)

    #distance_dict = generate_distance_dict(point_dict)
    #save_distance_dict(distance_dict, str(len(point_dict))+".cache")
    #plot_result(greedy_solution, point_dict)

    # prepare the solution in the specified output format
    output_data = '%.2f' % greedy_result + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, greedy_solution))
    # plot_result(greedy_solution,point_dict)
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

