from collections import namedtuple
from A5_facility.facility_caching import *
from facility_util import *
from facility_localsearch import *
from copy import deepcopy
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
    original_facilities = deepcopy(facilities)
    global_cost = facility_greedy(facilities, customers, facility_cache);
    current_cost = global_cost
    global_solution = generate_output_array_from_solution(global_cost,customers)
    opened_facilities_index = get_opened_facilities(customers)
    build_facility_customer_list(facilities,customers)

    initial_temperature_dict = {
        "200_800" : 1500,
        "500_3000": 2000, # need to tune this
        "100_1000": 1500,
        "1000_1500": 1500,
        "2000_2000": 1200
    }
    initial_iteration_dict = {
        "25_50": 10,
        "50_200": 24000000,
        "100_100": 10,
        "100_1000": 2000000,
        "200_800": 24000000,
        "500_3000": 24000000,
        "1000_1500": 24000000,
        "2000_2000": 24000000
    }
    temeperature_key = str(len(facilities))+"_"+str(len(customers))
    max_iteration = 24000000
    initial_temperature = 3500
    if temeperature_key in initial_temperature_dict:
        initial_temperature = initial_temperature_dict[temeperature_key]
    if temeperature_key in initial_iteration_dict:
        max_iteration = initial_iteration_dict[temeperature_key]
    swap_count = 1
    quenching_cycle_count = 10
    average_delta = 0
    max_reheat_count = 5
    is_reheat = False
    current_reheat_count = max_reheat_count
    def temerature(iteration, max_iteration):
        return initial_temperature * (1-iteration/max_iteration)

    def quench_temerature(iteration, max_iteration, quenching_cycle_count):
        quenching_period = max_iteration/quenching_cycle_count
        return initial_temperature * (math.sin(2*math.pi/quenching_period*iteration + 0.5*math.pi)*0.4 + 0.6)

    iteration = 0
    #print("Initial Temperature {0}".format(initial_temperature))
    while iteration < max_iteration:
        current_temperature = temerature(iteration,max_iteration)
        #current_temperature = quench_temerature(iteration,max_iteration, quenching_cycle_count)
        # delta_cost, facility_changes,customers_changes = \
        #     facility_reassign(facilities,customers,swap_count,facility_cache,opened_facilities_index)
        if iteration %2 == 1:
            delta_cost, facility_changes,customers_changes = \
                facility_swap(facilities,customers,facility_cache,opened_facilities_index)
        else:
            delta_cost, facility_changes, customers_changes = \
                facility_reassign(facilities, customers,swap_count,facility_cache, opened_facilities_index)
        if acceptance(delta_cost, current_temperature) >= random.random():
            if average_delta == 0:
                average_delta = abs(delta_cost)
            else:
                average_delta += abs(delta_cost)
                average_delta /= 2

            #print("Current Cost: {0}".format(current_cost))
            for facility_index in facility_changes:
                facilities[facility_index].capacity += facility_changes[facility_index]
                if facility_index not in opened_facilities_index:
                    opened_facilities_index.add(facility_index)
                if facilities[facility_index].capacity >= facilities[facility_index].max_capacity:
                    opened_facilities_index.remove(facility_index)
            for customers_index in customers_changes:
                customers[customers_index].assigned_facility = customers_changes[customers_index][1]
                if customers_index in facilities[customers_changes[customers_index][0]].customers:
                    facilities[customers_changes[customers_index][0]].customers.remove(customers_index)
                facilities[customers_changes[customers_index][1]].customers.append(customers_index)
            if current_cost + delta_cost < global_cost:
                global_solution = generate_output_array_from_solution(current_cost+delta_cost,customers)
                global_cost = current_cost+delta_cost
                cost = get_cost_and_capacity(deepcopy(original_facilities), customers, facility_cache)
                assert abs(global_cost - cost) <= 10
                print("Cost: {0}, Iteration: {1}, Average Delta: {2}".format(global_cost, iteration/max_iteration, average_delta))
            current_cost += delta_cost
        iteration+=1
        if is_reheat:
            if iteration == max_iteration:
                if current_reheat_count == 0:
                    break
                # reheat
                print("[Reheat] Current Result: {0}".format(global_cost))
                current_reheat_count -= 1
                iteration = int(current_reheat_count/max_reheat_count)


    return global_solution


