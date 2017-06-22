from vrp_structs import  vrp_problem_context,vrp_solution
from vrp_cache import vrp_cache
import  sys
def vrp_greedy(problem_context : vrp_problem_context, problem_cach : vrp_cache):
    solution = vrp_solution(problem_context.vehicle_count,problem_context.vehicle_max_capacity)
    for customer in problem_context.customers:
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