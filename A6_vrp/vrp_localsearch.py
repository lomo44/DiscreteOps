from vrp_structs import vrp_solution, vrp_problem_context
from vrp_cache import vrp_cache
import random
from enum import Enum


class vrp_local_search_type(Enum):
    vrp_swap = 0
    vrp_move = 1
    vrp_trade = 3


class vrp_local_search_context(object):
    def __init__(self, local_search_type: vrp_local_search_type):
        if local_search_type == vrp_local_search_type.vrp_swap:
            self.estimate_function = vrp_local_search_swap_estimate
            self.apply_function = vrp_local_search_swap_apply
        elif local_search_type == vrp_local_search_type.vrp_trade:
            self.estimate_function = vrp_local_search_trade_estimate
            self.apply_function = vrp_local_search_trade_apply
        elif local_search_type == vrp_local_search_type.vrp_move:
            self.estimate_function = vrp_local_search_move_estimate
            self.apply_function = vrp_local_search_move_apply
        else:
            self.estimate_function = None
            self.apply_function = None
        self.structure_changes = {}
        self.cost_delta = 0

    def has_changes(self):
        return len(self.structure_changes) != 0

    def get_estimate(self, current_solution, problem_context, problem_cache):
        self.estimate_function(current_solution, problem_context, self, problem_cache)

    def apply_changes(self, solution: vrp_solution, problem_context: vrp_problem_context):
        if self.apply_function is not None:
            self.apply_function(solution, self, problem_context)


def vrp_local_search_swap_estimate(vehicle_list: vrp_solution, problem_context,
                                   search_context: vrp_local_search_context, problem_cache: vrp_cache):
    vehicle_picks = set(range(vehicle_list.vehicle_count))
    while len(vehicle_picks) != 0:
        vehicle_pick = random.sample(vehicle_picks, 1)[0]
        vehicle_picks.remove(vehicle_pick)
        vehicle_schedule = vehicle_list.vehicle_schedule[vehicle_pick]
        if len(vehicle_schedule) > 2:
            swap_selection = set(range(len(vehicle_schedule)))
            swap_lower = random.sample(swap_selection, 1)[0]
            swap_selection.remove(swap_lower)
            swap_upper = random.sample(swap_selection, 1)[0]
            while swap_upper == (swap_lower + len(vehicle_schedule) - 1) % len(vehicle_schedule):
                swap_selection.remove(swap_upper)
                swap_upper = random.sample(swap_selection, 1)[0]

            previous_cost = \
                problem_cache.get_distance_between_customers(vehicle_schedule[swap_lower], vehicle_schedule[
                    (swap_lower + len(vehicle_schedule) - 1) % len(vehicle_schedule)]) + \
                problem_cache.get_distance_between_customers(vehicle_schedule[swap_upper], vehicle_schedule[
                    (swap_upper + len(vehicle_schedule) + 1) % len(vehicle_schedule)])
            current_cost = \
                problem_cache.get_distance_between_customers(vehicle_schedule[swap_lower], vehicle_schedule[
                    (swap_upper + len(vehicle_schedule) + 1) % len(vehicle_schedule)]) + \
                problem_cache.get_distance_between_customers(vehicle_schedule[swap_upper], vehicle_schedule[
                    (swap_lower + len(vehicle_schedule) - 1) % len(vehicle_schedule)])
            search_context.cost_delta = current_cost - previous_cost
            search_context.structure_changes[vehicle_pick] = (swap_lower, swap_upper)
            break


def vrp_local_search_swap_apply(current_solution: vrp_solution, search_context: vrp_local_search_context,
                                problem_context: vrp_problem_context):
    if len(search_context.structure_changes) != 0:
        for vehicle in search_context.structure_changes:
            lower = search_context.structure_changes[vehicle][0]
            upper = search_context.structure_changes[vehicle][1]
            target_schedule = current_solution.vehicle_schedule[vehicle]
            if lower < upper:
                target_schedule[lower:upper + 1] = target_schedule[lower:upper + 1][::-1]
            if lower > upper:
                while lower != len(target_schedule) and upper != -1:
                    target_schedule[lower], target_schedule[upper] = target_schedule[upper], target_schedule[lower]
                    lower += 1
                    upper -= 1
                if lower != len(target_schedule):
                    target_schedule[lower:len(target_schedule)] = target_schedule[lower:len(target_schedule)][::-1]
                if upper != -1:
                    target_schedule[0:upper + 1] = target_schedule[0:upper + 1][::-1]
            current_solution.current_cost += search_context.cost_delta
            break


def vrp_local_search_move_estimate(vehicle_list: vrp_solution, problem_context,
                                   search_context: vrp_local_search_context, problem_cache: vrp_cache):
    source_vehicles_set = set(range(vehicle_list.vehicle_count))
    while len(source_vehicles_set) != 0:
        src_vehicle_pick = random.sample(source_vehicles_set, 1)[0]
        source_vehicles_set.remove(src_vehicle_pick)
        src_vehicle_customers = vehicle_list.vehicle_schedule[src_vehicle_pick]
        source_vehicle_customers_set = set(range(len(src_vehicle_customers)))
        while len(source_vehicle_customers_set) != 0:
            src_vehicle_customer = random.sample(source_vehicle_customers_set, 1)[0]
            source_vehicle_customers_set.remove(src_vehicle_customer)
            if src_vehicle_customers[src_vehicle_customer] != 0:
                dst_vehicles_set = set(range(vehicle_list.vehicle_count))
                dst_vehicles_set.remove(src_vehicle_pick)
                while len(dst_vehicles_set) != 0:
                    dst_vehicle_pick = random.sample(dst_vehicles_set, 1)[0]
                    dst_vehicles_set.remove(dst_vehicle_pick)
                    dst_vehicle_customers = vehicle_list.vehicle_schedule[dst_vehicle_pick]
                    if vehicle_list.current_capacity[dst_vehicle_pick] >= problem_context.customers[
                        src_vehicle_customers[src_vehicle_customer]].demand:
                        search_context.structure_changes = (src_vehicle_pick, src_vehicle_customer, dst_vehicle_pick)
                        search_context.cost_delta -= problem_cache.get_distance_between_customers(
                            src_vehicle_customers[src_vehicle_customer], src_vehicle_customers[
                                (src_vehicle_customer + len(src_vehicle_customers) - 1) % len(
                                    src_vehicle_customers)])
                        search_context.cost_delta -= problem_cache.get_distance_between_customers(
                            src_vehicle_customers[src_vehicle_customer], src_vehicle_customers[
                                (src_vehicle_customer + len(src_vehicle_customers) + 1) % len(
                                    src_vehicle_customers)])
                        search_context.cost_delta += problem_cache.get_distance_between_customers(
                            src_vehicle_customers[
                                (src_vehicle_customer + len(src_vehicle_customers) - 1) % len(
                                    src_vehicle_customers)], src_vehicle_customers[
                                (src_vehicle_customer + len(src_vehicle_customers) + 1) % len(
                                    src_vehicle_customers)])
                        search_context.cost_delta += problem_cache.get_distance_between_customers(
                            dst_vehicle_customers[0], src_vehicle_customers[src_vehicle_customer])
                        search_context.cost_delta += problem_cache.get_distance_between_customers(
                            dst_vehicle_customers[-1], src_vehicle_customers[src_vehicle_customer])
                        search_context.cost_delta -= problem_cache.get_distance_between_customers(
                            dst_vehicle_customers[-1], dst_vehicle_customers[0])
                        return


def vrp_local_search_move_apply(current_solution: vrp_solution, search_context: vrp_local_search_context,
                                problem_context: vrp_problem_context):
    if search_context.has_changes():
        src_vehicle_pick = search_context.structure_changes[0]
        src_vehicle_customer = search_context.structure_changes[1]
        dst_vehicle_pick = search_context.structure_changes[2]

        current_solution.current_capacity[src_vehicle_pick] += problem_context.customers[
            current_solution.vehicle_schedule[src_vehicle_pick][src_vehicle_customer]].demand
        current_solution.current_capacity[dst_vehicle_pick] -= problem_context.customers[
            current_solution.vehicle_schedule[src_vehicle_pick][src_vehicle_customer]].demand

        current_solution.vehicle_schedule[dst_vehicle_pick].append(
            current_solution.vehicle_schedule[src_vehicle_pick][src_vehicle_customer])
        del current_solution.vehicle_schedule[src_vehicle_pick][src_vehicle_customer]
        current_solution.current_cost += search_context.cost_delta


def vrp_local_search_trade_estimate(vehicle_list: vrp_solution, problem_context:vrp_problem_context,
                                    search_context: vrp_local_search_context, problem_cache: vrp_cache):
    def check_swappable(src_vehicle, src_customer, dst_vehicle, dst_customer):
        if vehicle_list.current_capacity[src_vehicle] + problem_context.customers[src_customer].demand - \
                problem_context.customers[dst_customer].demand >= 0\
                and vehicle_list.current_capacity[dst_vehicle] + problem_context.customers[dst_customer].demand \
                        - problem_context.customers[src_customer].demand >= 0:
            return True
        return False

    src_vehicles_set = set(range(vehicle_list.vehicle_count))
    while len(src_vehicles_set) != 0:
        src_vehicle_pick = random.sample(src_vehicles_set, 1)[0]
        src_vehicles_set.remove(src_vehicle_pick)
        src_vehicle_customers = vehicle_list.vehicle_schedule[src_vehicle_pick]
        src_vehicle_customers_set = set(range(len(src_vehicle_customers)))
        while len(src_vehicle_customers_set) != 0:
            src_vehicle_customer = random.sample(src_vehicle_customers_set, 1)[0]
            src_vehicle_customers_set.remove(src_vehicle_customer)
            if src_vehicle_customers[src_vehicle_customer] != 0:
                dst_vehicles_set = set(range(vehicle_list.vehicle_count))
                dst_vehicles_set.remove(src_vehicle_pick)
                while len(dst_vehicles_set) != 0:
                    dst_vehicle_pick = random.sample(dst_vehicles_set, 1)[0]
                    dst_vehicles_set.remove(dst_vehicle_pick)
                    dst_vehicle_customers = vehicle_list.vehicle_schedule[dst_vehicle_pick]
                    dst_vehicle_customers_set = set(range(len(dst_vehicle_customers)))
                    while len(dst_vehicle_customers_set) != 0:
                        dst_vehicle_customer = random.sample(dst_vehicle_customers_set, 1)[0]
                        dst_vehicle_customers_set.remove(dst_vehicle_customer)
                        if dst_vehicle_customers[dst_vehicle_customer] != 0:
                            if check_swappable(src_vehicle_pick, src_vehicle_customers[src_vehicle_customer],
                                               dst_vehicle_pick, dst_vehicle_customers[dst_vehicle_customer]):
                                search_context.structure_changes = (
                                    src_vehicle_pick, src_vehicle_customer, dst_vehicle_pick, dst_vehicle_customer)
                                search_context.cost_delta -= problem_cache.get_distance_between_customers(
                                    src_vehicle_customers[src_vehicle_customer], src_vehicle_customers[
                                        (src_vehicle_customer + len(src_vehicle_customers) - 1) % len(
                                            src_vehicle_customers)])
                                search_context.cost_delta -= problem_cache.get_distance_between_customers(
                                    src_vehicle_customers[src_vehicle_customer], src_vehicle_customers[
                                        (src_vehicle_customer + len(src_vehicle_customers) + 1) % len(
                                            src_vehicle_customers)])
                                search_context.cost_delta += problem_cache.get_distance_between_customers(
                                    dst_vehicle_customers[dst_vehicle_customer], src_vehicle_customers[
                                        (src_vehicle_customer + len(src_vehicle_customers) - 1) % len(
                                            src_vehicle_customers)])
                                search_context.cost_delta += problem_cache.get_distance_between_customers(
                                    dst_vehicle_customers[dst_vehicle_customer], src_vehicle_customers[
                                        (src_vehicle_customer + len(src_vehicle_customers) + 1) % len(
                                            src_vehicle_customers)])

                                search_context.cost_delta -= problem_cache.get_distance_between_customers(
                                    dst_vehicle_customers[dst_vehicle_customer], dst_vehicle_customers[
                                        (dst_vehicle_customer + len(dst_vehicle_customers) - 1) % len(
                                            dst_vehicle_customers)])
                                search_context.cost_delta -= problem_cache.get_distance_between_customers(
                                    dst_vehicle_customers[dst_vehicle_customer], dst_vehicle_customers[
                                        (dst_vehicle_customer + len(dst_vehicle_customers) + 1) % len(
                                            dst_vehicle_customers)])
                                search_context.cost_delta += problem_cache.get_distance_between_customers(
                                    src_vehicle_customers[src_vehicle_customer], dst_vehicle_customers[
                                        (dst_vehicle_customer + len(dst_vehicle_customers) - 1) % len(
                                            dst_vehicle_customers)])
                                search_context.cost_delta += problem_cache.get_distance_between_customers(
                                    src_vehicle_customers[src_vehicle_customer], dst_vehicle_customers[
                                        (dst_vehicle_customer + len(dst_vehicle_customers) + 1) % len(
                                            dst_vehicle_customers)])

                                return


def vrp_local_search_trade_apply(current_solution: vrp_solution, search_context: vrp_local_search_context,
                                 problem_context: vrp_problem_context):
    if len(search_context.structure_changes) != 0:
        src_vehicle_pick = search_context.structure_changes[0]
        src_vehicle_customer = search_context.structure_changes[1]
        dst_vehicle_pick = search_context.structure_changes[2]
        dst_vehicle_customer = search_context.structure_changes[3]
        src_vehicle_schedule = current_solution.vehicle_schedule[src_vehicle_pick]
        dst_vehicle_schedule = current_solution.vehicle_schedule[dst_vehicle_pick]

        current_solution.current_capacity[src_vehicle_pick] += problem_context.customers[src_vehicle_schedule[src_vehicle_customer]].demand
        current_solution.current_capacity[src_vehicle_pick] -= problem_context.customers[dst_vehicle_schedule[dst_vehicle_customer]].demand

        current_solution.current_capacity[dst_vehicle_pick] += problem_context.customers[dst_vehicle_schedule[dst_vehicle_customer]].demand
        current_solution.current_capacity[dst_vehicle_pick] -= problem_context.customers[src_vehicle_schedule[src_vehicle_customer]].demand

        current_solution.vehicle_schedule[src_vehicle_pick][src_vehicle_customer], \
        current_solution.vehicle_schedule[dst_vehicle_pick][dst_vehicle_customer] = \
            current_solution.vehicle_schedule[dst_vehicle_pick][dst_vehicle_customer], \
            current_solution.vehicle_schedule[src_vehicle_pick][src_vehicle_customer]

        current_solution.current_cost += search_context.cost_delta
