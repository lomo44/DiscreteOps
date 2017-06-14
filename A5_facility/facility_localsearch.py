import random


def facility_reassign(facilities, customers, swap_count, facility_cache, opened_facility_index):
    delta_cost = 0

    real_swap_count = min(len(customers)/2, int(swap_count))
    used_customers_index = set()

    facility_capacity_changes = {}
    customer_facility_changes = {}

    # pull out the customers from index
    while real_swap_count != 0:
        select_index = random.randint(0,len(customers)-1)
        if select_index not in used_customers_index:
            real_swap_count-=1
            used_customers_index.add(select_index)
            if customers[select_index].assigned_facility != -1:
                if customers[select_index].assigned_facility not in facility_capacity_changes:
                    facility_capacity_changes[customers[select_index].assigned_facility] = 0
                if select_index not in customer_facility_changes:
                    customer_facility_changes[select_index] = [customers[select_index].assigned_facility, -1]
                facility_capacity_changes[customers[select_index].assigned_facility] += customers[select_index].demand
            else:
                return
    # reassign facility
    for index in used_customers_index:
        # get possible facility
        possible_facility = set(range(0,len(facilities)))
        select_index = None
        while len(possible_facility) != 0:
            current_index = random.randint(0, len(possible_facility) - 1)
            if current_index in possible_facility and current_index != customer_facility_changes[index][0]:
                addtional_capacity = 0
                if current_index in facility_capacity_changes:
                    addtional_capacity = facility_capacity_changes[current_index]
                if facilities[current_index].capacity + addtional_capacity >= customers[index].demand:
                    select_index = current_index
                    break
                else:
                    possible_facility.remove(current_index)
        customer_facility_changes[index][1] = select_index
        if select_index not in facility_capacity_changes:
            facility_capacity_changes[select_index] = 0
        facility_capacity_changes[select_index] -= customers[index].demand

    facility_capacity_changes = {k: v for k, v in facility_capacity_changes.items() if v != 0}

    for facility_index in facility_capacity_changes:
        if facility_index not in opened_facility_index:
            delta_cost += facilities[facility_index].setup_cost
        if facilities[facility_index].capacity + facility_capacity_changes[facility_index] >= facilities[facility_index].max_capacity:
            delta_cost -= facilities[facility_index].setup_cost

    for customer_index in customer_facility_changes:
        delta_cost += facility_cache.distance_cache[customer_index][customer_facility_changes[customer_index][1]]-\
                      facility_cache.distance_cache[customer_index][customer_facility_changes[customer_index][0]]
    return delta_cost, facility_capacity_changes, customer_facility_changes

