from collections import namedtuple
from A5_facility.facility_caching import *
from A5_facility.facility_util import *


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
    global_cost = facility_greedy(facilities, customers, facility_cache);

    max_iteration = 1000
    initial_temperature = 10

    def temerature(iteration, max_iteration):
        return initial_temperature * (1-iteration/max_iteration)

    for iteration in range(0,max_iteration):
        current_temperature = temerature(iteration,max_iteration)
        