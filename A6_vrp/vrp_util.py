# utility function sets for vrp problem
from collections import namedtuple
from vrp_structs import vrp_problem_context,vrp_solution
from vrp_cache import vrp_cache
Customer = namedtuple("Customer", ['index', 'demand', 'x', 'y'])


def parse_input_data_from_file(input_file):
    with open(input_file, 'r') as _file:
        return parse_input_data_from_string(_file.read())

def parse_input_data_from_string(input_data):
    lines = input_data.split('\n')

    parts = lines[0].split()
    customer_count = int(parts[0])
    vehicle_count = int(parts[1])
    vehicle_capacity = int(parts[2])
    customers = []
    for i in range(1, customer_count+1):
        line = lines[i]
        parts = line.split()
        customers.append(Customer(i-1, int(parts[0]), float(parts[1]), float(parts[2])))

    #the depot is always the first customer in the input
    depot = customers[0]
    return_context = vrp_problem_context()
    return_context.depot = depot
    return_context.vehicle_count = vehicle_count
    return_context.vehicle_max_capacity = vehicle_capacity
    return_context.customers = customers

    return return_context

def check_solution_valid(input_problem_context:vrp_problem_context, vehicle_list:vrp_solution):
    for vehicle in vehicle_list.vehicle_schedule:
        current_demands = sum(customer.demand for customer in vehicle)
        if current_demands > vehicle_list.vehicle_capacity:
            return False
    return True

def get_solution_cost(input_problem_context:vrp_problem_context, vehicle_list:vrp_solution, problem_cache:vrp_cache):
    return_cost = 0
    for vehicle in vehicle_list.vehicle_schedule:
        if len(vehicle) >= 1:
            for index in range(len(vehicle)-1):
                return_cost += problem_cache.get_distance_between_customers(vehicle[index],vehicle[index+1])
            return_cost += problem_cache.get_distance_between_customers(0,1)
            return_cost += problem_cache.get_distance_between_customers(0,-1)
    return return_cost

        
    