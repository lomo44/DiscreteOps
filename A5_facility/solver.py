#!/usr/bin/python
# -*- coding: utf-8 -*-

from facility_solver import *
from facility_util import load_cache
import math

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def solve_it(input_data):

    # parse the input
    facilities,customers = parse_input_from_string(input_data)
    facilities_cache = load_cache(str(len(facilities))+"_"+str(len(customers))+".cache")
    #cost = facility_greedy(facilities,customers,facilities_cache)
    #return generate_output_from_solution(cost,customers)
    return genereate_output_from_output_array(facility_SA(facilities,customers,facilities_cache))


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/fl_16_2)')

