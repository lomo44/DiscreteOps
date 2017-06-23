#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from collections import namedtuple
from vrp_util import parse_input_data_from_string
from vrp_cache import vrp_cache
from vrp_solver import  vrp_greedy, vrp_sa
Customer = namedtuple("Customer", ['index', 'demand', 'x', 'y'])

def length(customer1, customer2):
    return math.sqrt((customer1.x - customer2.x)**2 + (customer1.y - customer2.y)**2)

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    problem_context = parse_input_data_from_string(input_data)
    problem_cache = vrp_cache()
    problem_cache.generate_cache(problem_context)
    solution = vrp_sa(problem_context,problem_cache)

    return solution.generate_output_string()


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:

        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/vrp_5_4_1)')

