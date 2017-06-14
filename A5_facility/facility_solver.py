from collections import namedtuple
from A5_facility.facility_caching import *
from facility_util import *
from facility_localsearch import *

def facility_greedy(facilities, customers, facility_cache):

    openedFacility = set()
    openedFacility_index = set()
    current_cost = 0
    for customer in customers:
        join_cost, join_facility= get_nearest_joinable_facility(openedFacility,customer,facility_cache.distance_cache)

        reopen_cost = None
        new_facility_index = get_nearest_facility(customer,facilities,openedFacility_index,facility_cache)
        if new_facility_index is not None:
            reopen_cost = facility_cache.cost_cache[customer.index][new_facility_index]
        if reopen_cost is not None or join_facility is not None:
            if reopen_cost is None and join_facility is not None:
                join_facility.capacity -= customer.demand
                current_cost += join_cost
                customer.assigned_facility = join_facility.index
            elif reopen_cost is not None and join_facility is None:
                facilities[new_facility_index].capacity -= customer.demand
                current_cost += reopen_cost
                openedFacility_index.add(facilities[new_facility_index].index)
                openedFacility.add(facilities[new_facility_index])
                customer.assigned_facility = facilities[new_facility_index].index
            else:
                if join_cost > reopen_cost:
                    facilities[new_facility_index].capacity -= customer.demand
                    current_cost += reopen_cost
                    openedFacility_index.add(facilities[new_facility_index].index)
                    openedFacility.add(facilities[new_facility_index])
                    customer.assigned_facility = facilities[new_facility_index].index
                else:
                    join_facility.capacity -= customer.demand
                    current_cost += join_cost
                    customer.assigned_facility = join_facility.index
    return current_cost


def facility_SA(facilities, customers, facility_cache):

    def acceptance(delta, temperature):
        if delta < 0:
            return 1
        else:
            return math.exp(-delta/temperature)

    global_cost = facility_greedy(facilities, customers, facility_cache);
    current_cost = global_cost
    global_solution = generate_output_from_solution(global_cost,customers)
    opened_facilities_index = get_opened_facilities(customers)

    max_iteration = 4000
    initial_temperature = 1
    swap_count = 1

    def temerature(iteration, max_iteration):
        return initial_temperature * (1-iteration/max_iteration)

    for iteration in range(0,max_iteration):
        current_temperature = temerature(iteration,max_iteration)
        delta_cost, facility_changes,customers_changes = \
            facility_reassign(facilities,customers,swap_count,facility_cache,opened_facilities_index)
        if acceptance(delta_cost, current_temperature):
            #print("Current Cost: {0}".format(current_cost))
            for facility_index in facility_changes:
                facilities[facility_index].capacity += facility_changes[facility_index]
                if facility_index not in opened_facilities_index:
                    opened_facilities_index.add(facility_index)
                if facilities[facility_index].capacity >= facilities[facility_index].max_capacity:
                    opened_facilities_index.remove(facility_index)
            for customers_index in customers_changes:
                customers[customers_index].assigned_facility = customers_changes[customers_index][1]
            if current_cost + delta_cost < global_cost:
                global_solution = generate_output_from_solution(current_cost+delta_cost,customers)
                global_cost = current_cost+delta_cost
                print("Cost: {0}, Iteration: {1}".format(global_cost, iteration/max_iteration))
            current_cost += delta_cost
    return global_solution


