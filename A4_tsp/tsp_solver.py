from A4_tsp.tsp_util import *
import sys
import random

def tsp_master(point_dict, distance_dict):
    distance,result = tsp_greedy_ex(point_dict,distance_dict,int(len(point_dict)/4))
    return distance,result

def tsp_greedy(point_dict, distance_dict,start_index):
    total_distance = 0;
    solution_sequence = []
    current_index = start_index
    available_set = set(point_dict.keys())
    while len(available_set)!=0:
        solution_sequence.append(current_index)
        available_set.remove(current_index)
        if len(available_set) == 0:
            break
        shortest_distance = sys.maxsize
        shortest_index = -1
        for item in available_set:
            sub_distance = get_distance_from_dict(current_index, item, distance_dict)
            if sub_distance < shortest_distance:
                shortest_distance = sub_distance
                shortest_index = item
        current_index = shortest_index
        total_distance += shortest_distance
    total_distance += get_distance_from_dict(solution_sequence[0],solution_sequence[len(solution_sequence)-1],distance_dict)
    return total_distance,solution_sequence

def tsp_greedy_ex(point_dict, distance_dict, iteration):
    starting_points = random.sample(range(len(point_dict)),iteration)
    best_result = sys.maxsize
    best_solution = None
    for starting_point in starting_points:
        temp_distance,temp_solution = tsp_greedy(point_dict,distance_dict,starting_point)
        if temp_distance < best_result:
            best_result = temp_distance
            best_solution = temp_solution
    return best_result,best_solution

def tsp_sa(point_dict, distance_dict):
    def generate_initial_solution(point_dict, distance):
        return tsp_greedy_ex(point_dict,distance_dict,len(point_dict)/4)
    def generate_initial_temperature(solution):
        return len(solution)

    max_search_iteration = len(point_dict)

    current_result, current_solution = generate_initial_solution(point_dict,distance_dict)
    for index in range(0, max_search_iteration):
        pass
    pass