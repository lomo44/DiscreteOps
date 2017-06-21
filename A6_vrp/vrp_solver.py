from vrp_structs import  vrp_problem_context,vrp_solution
from vrp_cache import vrp_cache
import  sys
def vrp_greedy(problem_context : vrp_problem_context, problem_cach : vrp_cache):
    solution = vrp_solution(problem_context.)

    for customer in problem_context.customers:
        assigned_vehicle = None
        min_distance = sys.maxsize
        for vehicle in v