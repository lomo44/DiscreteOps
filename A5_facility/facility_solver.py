from collections import namedtuple
from A5_facility.facility_caching import *
from A5_facility.facility_util import *

Facility = namedtuple("Facility", ['index', 'setup_cost', 'capacity', 'location'])


def facility_greedy(facilities, customers):

    distance_cache, order_cache = load_caches(facilities, customers)

    openedFacility = set()
    openedFacility_index = set()
    current_cost = 0
    for customer in customers:
        join_cost, join_facility= get_nearest_joinable_facility(openedFacility,customer,distance_cache)

        reopen_cost = None
        new_facility_index = get_nearest_unopened_facility(openedFacility_index,customer, order_cache, facilities)
        if new_facility_index is not None:
            reopen_cost = facilities[new_facility_index].setup_cost + get_distance_from_dict(facilities[new_facility_index],
                                                                                   customer,distance_cache)
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

