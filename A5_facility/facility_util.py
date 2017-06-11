from A5_facility.facility_caching import *
import sys
def get_nearest_joinable_facility(facilities, customer, distance_dict):
    result_cost = sys.maxsize
    result_facility = None
    for facility in facilities:
        if facility.capacity >= customer.demand:
            current_cost = get_distance_from_dict(facility, customer,distance_dict)
            if current_cost < result_cost:
                result_cost = current_cost
                result_facility = facility
    return result_cost, result_facility

def get_nearest_unopened_facility(open_facilities_index,customer,order_cache, facilities):
    order_list = order_cache[customer.index]
    unopen_list = list(filter(
        lambda x: x not in open_facilities_index and facilities[x].capacity >= customer.demand, order_list))
    if len(unopen_list) >= 1:
        return unopen_list[0]
    return None

def generate_output_from_solution(cost, customers):
    solution = [0] * len(customers)
    for customer in customers:
        solution[customer.index] = customer.assigned_facility
    output_data = '%.2f' % cost + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))
    return output_data