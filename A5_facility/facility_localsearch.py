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

def facility_swap(facilities, customers, facility_cache, opened_facility_index):

    def check_swappable(customer_A, customer_B):
        if facilities[customer_A.assigned_facility].capacity + customer_A.demand >= customer_B.demand and \
                                facilities[customer_B.assigned_facility].capacity + customer_B.demand >= customer_A.demand:
            return True
        return False

    def get_possible_facilities(customer_A, _facilities):
        return list(map(lambda x: x.index, filter(lambda y: y.max_capacity >= customer_A.demand and y.index != customer_A.assigned_facility, _facilities)))

    G_CA = None
    G_FB = None
    G_CB = None
    possible_customer_A = set(range(len(customers)))

    while len(possible_customer_A) > 0:
        pick_CA = random.sample(possible_customer_A,1)[0]
        possible_facility = get_possible_facilities(customers[pick_CA], facilities)
        while len(possible_facility) > 0:
            pick_FA = random.sample(possible_facility,1)[0]
            if facilities[pick_FA].capacity >= customers[pick_CA].demand:
                if len(facilities[pick_FA].customers) == 0:
                    G_FB = pick_FA
                    G_CB = -1
                    break
                else:
                    possible_CB = set(range(len(facilities[pick_FA].customers)))
                    while len(possible_CB) >0:
                        pick_FB = random.sample(possible_CB,1)[0]
                        if check_swappable(customers[pick_FA],customers[facilities[pick_FA].customers[pick_FB]]):
                            G_FB = pick_FA
                            G_CB = customers[facilities[pick_FA].customers[pick_FB]].index
                            break
                        else:
                            possible_CB.remove(pick_FB)
            if G_FB is not None and G_CB is not None:
                break
            else:
                possible_facility.remove(pick_FA)

        if G_FB is not None:
            G_CA = pick_CA
            break
        else:
            possible_customer_A.remove(pick_CA)

    # calculate costs
    delta_cost = 0
    facility_capacity_changes = {}
    customer_facility_changes = {}


    if G_CA is not None and G_FB is not None:
        customer_facility_changes[G_CA] = (customers[G_CA].assigned_facility, G_FB)
        facility_capacity_changes[customers[G_CA].assigned_facility] = customers[G_CA].demand
        facility_capacity_changes[G_FB] = -customers[G_CA].demand
        delta_cost += (facility_cache.distance_cache[G_CA][G_FB]-facility_cache.distance_cache[G_CA][customers[G_CA].assigned_facility])
        if G_CB == -1:
            if customers[G_CA].demand + facilities[customers[G_CA].assigned_facility].capacity >= facilities[
                customers[G_CA].assigned_facility].max_capacity:
                delta_cost -= facilities[customers[G_CA].assigned_facility].setup_cost
            delta_cost += facilities[G_FB].setup_cost
        else:
            customer_facility_changes[G_CB] = (G_FB, customers[G_CA].assigned_facility)
            facility_capacity_changes[customers[G_CA].assigned_facility] += -customers[G_CB].demand
            facility_capacity_changes[G_FB] += customers[G_CB].demand
            # if customers[G_CB].demand + facilities[customers[G_CB].assigned_facility].capacity >= facilities[customers[G_CB].assigned_facility].max_capacity:
            #     delta_cost -= facilities[customers[G_CB].assigned_facility].setup_cost
            delta_cost += (facility_cache.distance_cache[G_CB][
                customers[G_CA].assigned_facility]-facility_cache.distance_cache[G_CB][G_FB])

    facility_capacity_changes = {k: v for k, v in facility_capacity_changes.items() if v != 0}
    return delta_cost,facility_capacity_changes,customer_facility_changes

