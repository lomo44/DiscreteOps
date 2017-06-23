from vrp_structs import  vrp_problem_context,vrp_solution
from vrp_cache import vrp_cache
from vrp_localsearch import vrp_local_search_context,vrp_local_search_type
import  sys
import  math
import random
def vrp_greedy(problem_context : vrp_problem_context, problem_cach : vrp_cache):
    solution = vrp_solution(problem_context.vehicle_count,problem_context.vehicle_max_capacity)
    sorted_customers = sorted(problem_context.customers, key=lambda x: x.demand, reverse=True)
    for customer in sorted_customers:
        assigned_vehicle = None
        min_distance = sys.maxsize
        if customer.index > 0:
            for vehicle_index, schedule in enumerate(solution.vehicle_schedule):
                if customer.demand <= solution.current_capacity[vehicle_index]:
                    current_distance = problem_cach.get_distance_between_customers(schedule[-1],customer.index)
                    if current_distance < min_distance:
                        min_distance = current_distance
                        assigned_vehicle = vehicle_index
            if assigned_vehicle is not None:
                solution.current_cost -= problem_cach.get_distance_between_customers(
                    solution.vehicle_schedule[assigned_vehicle][-1], solution.vehicle_schedule[assigned_vehicle][0])
                solution.current_cost += problem_cach.get_distance_between_customers(
                    solution.vehicle_schedule[assigned_vehicle][-1], customer.index)
                solution.current_cost += problem_cach.get_distance_between_customers(
                    solution.vehicle_schedule[assigned_vehicle][0], customer.index)
                solution.vehicle_schedule[assigned_vehicle].append(customer.index)
                solution.current_capacity[assigned_vehicle] -= customer.demand

            else:
                return None

    return solution

def vrp_sa(problem_context: vrp_problem_context, problem_cache: vrp_cache):
    current_solution = vrp_greedy(problem_context,problem_cache)

    initial_temperature_dict = {

    }

    initial_iteration_dict = {

    }
    problem_key = "_".join(map(lambda x: str(x),[problem_context.vehicle_count,problem_context.vehicle_max_capacity, len(problem_cache.customer_to_customer_cache)]))
    print("Current Problem Key: {0}".format(problem_key))
    max_iteration = 300000
    initial_temperature = 5
    if problem_key in initial_iteration_dict:
        initial_iteration = initial_iteration_dict[problem_key]
    if problem_key in initial_temperature_dict:
        initial_temperature = initial_temperature_dict[problem_key]

    def temperature(current_iteration, max_iteration):
        return initial_temperature * (1- current_iteration / max_iteration)
    def acceptance(delta, temperature):
        if delta < 0:
            return 1
        else:
            return math.exp(-delta/temperature)
    swap_bound = 0.3
    trade_bound = 0.7
    move_bound = 1.0

    current_iteration = 0
    while current_iteration < max_iteration:
        current_temperature = temperature(current_iteration,max_iteration)
        current_operation = random.random()
        search_context = None
        if current_operation <= swap_bound:
            search_context = vrp_local_search_context(vrp_local_search_type.vrp_swap)
        elif current_operation <= trade_bound:
            search_context = vrp_local_search_context(vrp_local_search_type.vrp_trade)
        elif current_operation <= move_bound:
            search_context = vrp_local_search_context(vrp_local_search_type.vrp_move)
        else:
            search_context = vrp_local_search_context(vrp_local_search_type.vrp_swap)

        search_context.get_estimate(current_solution,problem_context,problem_cache)
        if acceptance(search_context.cost_delta,current_temperature) >= random.random():
            search_context.apply_changes(current_solution,problem_context)
            print("Current cost: {0}".format(current_solution.current_cost))
        current_iteration += 1
    return current_solution