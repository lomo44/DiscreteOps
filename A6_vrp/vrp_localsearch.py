from vrp_structs import vrp_vehicle_list,vrp_problem_context
import random

def vrp_swap_feasibility_check(swap_A,swap_B,is_SwapA_Depot, is_SwapB_Depot, vrp_vehicle_list):
    return -1

def vrp_depot_check(index,input_list:vrp_vehicle_list):
    current_index = 0
    current_vehicle = 0
    while current_index < index:
        current_index+=1
        if current_index > index:
            return True
        else:
            current_index+=len(input_list.vehicle_schedule[current_vehicle])
            if current_index > index:
                return False
            else:
                current_vehicle+=1
    return True

def vrp_swap_estimate(input_list:vrp_vehicle_list, problem_context:vrp_problem_context):
    posible_picks_a = set(range(len(problem_context.customers)+problem_context.vehicle_list.vehicle_count))
    while len(posible_picks_a) != 0:
        pick_A = random.sample(posible_picks_a,1)
        posible_picks_b = set(range(len(problem_context.customers)+problem_context.vehicle_list.vehicle_count))
        posible_picks_b.remove(pick_A)
        pick_a_depot_check = vrp_depot_check(pick_A, input_list)
        while len(posible_picks_b) != 0:
            pick_B = random.sample(posible_picks_b,1)
            pick_b_depot_check = vrp_depot_check(pick_B, input_list)
            if pick_a_depot_check is True and pick_b_depot_check is True:
                break
            else:
                pass