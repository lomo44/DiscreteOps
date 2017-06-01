from A4_tsp.tsp_util import *

def get_2opt_delta(lower, upper, solution, distance_dict):
    if lower < upper and (upper - lower) == len(solution)-1:
        return 0
    if upper < lower and (lower - upper) == 1:
        return 0
    previous_cost = get_distance_from_dict(solution[lower], solution[(lower+len(solution)-1)%len(solution)], distance_dict) +\
        get_distance_from_dict(solution[upper], solution[(upper+len(solution)+1)%len(solution)],distance_dict)
    current_cost = get_distance_from_dict(solution[lower], solution[(upper+len(solution)+1)%len(solution)], distance_dict) +\
        get_distance_from_dict(solution[upper], solution[(lower+len(solution)-1)%len(solution)], distance_dict)
    return previous_cost-current_cost



def get_2opt(lower, upper, solution):
    if lower < upper:
        solution[lower:upper+1] = solution[lower:upper+1][::-1]
    if lower > upper:
        while lower != len(solution) and upper != -1:
            solution[lower],solution[upper] = solution[upper],solution[lower]
            lower+=1
            upper-=1
        if lower != len(solution):
            solution[lower:len(solution)] = solution[lower:len(solution)][::-1]
        if upper != -1:
            solution[0:upper+1] = solution[0:upper+1][::-1]
        pass
        # c = solution[lower:-upper-1]
        # lower_part = solution[lower:][::-1]
        # solution[lower:] = solution[:upper+1][::-1]
        # solution[:upper+1] = lower_part[:]
