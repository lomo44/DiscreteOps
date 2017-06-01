from A4_tsp.tsp_util import *
from A4_tsp.tsp_localsearch import *
import sys
import random

def tsp_master(point_dict, distance_dict):
    #distance,result = tsp_greedy_ex(point_dict,distance_dict,int(len(point_dict)/4))
    #return distance,result
    return tsp_sa(point_dict,distance_dict)

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

    def generate_initial_temperature(solution):
        return len(solution)


    def generate_local_search(solution):
        index1 = random.sample(range(len(solution)),1)[0]
        index2 = index1
        while index2 == index1:
            index2 = random.sample(range(len(solution)), 1)[0]
            # if test_index > index1 and test_index - index1 < len(solution)-1:
            #     index2 = test_index
            # if test_index < index1 and index1-index2 > 2:
            #     index2 = test_index
        return index1, index2

    def acceptance(delta, temperature):
        if delta > 0:
            return 1
        else:
            return math.exp(delta/temperature)

    max_search_iteration = 256000
    current_result, current_solution = tsp_greedy_ex(point_dict,distance_dict,int(len(point_dict)/4))
    temperature = 30
    zerocount = 0
    for index in range(0, max_search_iteration):
        current_temperature = temperature * (1-index/max_search_iteration)
        lower,upper = generate_local_search(current_solution)
        delta = get_2opt_delta(lower,upper,current_solution,distance_dict)
        if delta == 0:
            zerocount+=1
        if acceptance(delta, current_temperature) >= random.random():
            # accept new result
            current_result -= delta
            get_2opt(lower,upper,current_solution)
            current_result_2 = get_total_distance(current_solution, distance_dict)

            print("Current Result: {0}, Current Iteration: {1}".format(current_result, index))
    print("Zero Count: {0}".format(zerocount))
    return current_result, current_solution
