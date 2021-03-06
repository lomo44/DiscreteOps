
from facility_structs import *
from facility_caching import Facility_cache
import _pickle as cPickle
import sys
import math
import random
def get_distance_from_dict(facility, customer, distance_dict):
    return distance_dict[customer.index][facility.index]

def parse_input_from_string(input_data):
    lines = input_data.split('\n')
    parts = lines[0].split()
    facility_count = int(parts[0])
    customer_count = int(parts[1])

    facilities = []
    for i in range(1, facility_count + 1):
        parts = lines[i].split()
        new_facility = Facility()
        new_facility.index = i-1
        new_facility.setup_cost = float(parts[0])
        new_facility.capacity = int(parts[1])
        new_facility.max_capacity = int(parts[1])
        new_facility.location = Point(float(parts[2]), float(parts[3]))
        facilities.append(new_facility)

    customers = []
    for i in range(facility_count + 1, facility_count + 1 + customer_count):
        parts = lines[i].split()
        new_customer = Customer()
        new_customer.index = i - 1 - facility_count
        new_customer.demand = int(parts[0])
        new_customer.location = Point(float(parts[1]), float(parts[2]))
        new_customer.assigned_facility = -1
        customers.append(new_customer)
    return facilities,customers

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def parse_input_from_file(in_filePath):
    with open(in_filePath, 'r') as input_data_file:
        input_data = input_data_file.read()
        return parse_input_from_string(input_data)


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

def get_opened_facilities(_customers):
    ret_set = set()
    for customer in _customers:
        ret_set.add(customer.assigned_facility)
    return ret_set

def get_cost_and_capacity(facilities, customers, facility_cache):
    costs = 0.0
    opened_facility_set = set()
    for customer in customers:
        if customer.assigned_facility not in opened_facility_set:
            opened_facility_set.add(customer.assigned_facility)
            costs+=facilities[customer.assigned_facility].setup_cost
        facilities[customer.assigned_facility].capacity-=customer.demand
        costs+=facility_cache.distance_cache[customer.index][customer.assigned_facility]
    return costs


def get_nearest_facility(customer, facilities, excluded_facilities_index, facility_cache):
    for facility_index in facility_cache.distance_order_cache[customer.index]:
        if facility_index not in excluded_facilities_index and facilities[facility_index].capacity >= customer.demand:
            return facility_index
    return None

def get_cheapest_facility(customer, facilities, excluded_facilities_index, facility_cache):
    for facility_index in facility_cache.cost_order_cache[customer.index]:
        if facility_index not in excluded_facilities_index and facilities[facility_index].capacity >= customer.demand:
            return facility_index
    return None


def generate_output_from_solution(cost, customers):
    solution = [0] * len(customers)
    for customer in customers:
        solution[customer.index] = customer.assigned_facility
    output_data = '%.2f' % cost + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))
    return output_data

def generate_output_array_from_solution(cost, customers):
    return [cost] + list(map(lambda x:x.assigned_facility, customers))

def genereate_output_from_output_array(output_array):
    output_data = '%.2f' % output_array[0] + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, output_array[1:]))
    return output_data

def save_cache(self, output_file_path):
    with open(output_file_path, 'wb') as f:
        cPickle.dump(self, f)
    pass

def load_cache_from_count(facility_count, customer_count):
    return load_cache(str(facility_count)+"_"+str(customer_count)+".cache")

def load_cache(input_file_path):
    with open(input_file_path, 'rb') as f:
        return cPickle.load(f)

def build_facility_customer_list(facilities, customers):
    for customer in customers:
        facilities[customer.assigned_facility].customers.append(customer.index)

def check_solution_valid(facilities, customers):
    capacity_dict = {}
    for customer in customers:
        if customer.assigned_facility not in capacity_dict:
            capacity_dict[customer.assigned_facility] = 0
        capacity_dict[customer.assigned_facility] += customer.demand
        if capacity_dict[customer.assigned_facility] > facilities[customer.assigned_facility].max_capacity:
            print("Facility {0} capacity exceeded. Current: {1}, Max: {2}".format(customer.assigned_facility, capacity_dict[customer.assigned_facility], facilities[customer.assigned_facility].max_capacity))
            return False
    return True

def generate_caches():
    cachelist = [
        "./data/fl_3_1",
        "./data/fl_25_2",
        "./data/fl_50_6",
        "./data/fl_100_7",
        "./data/fl_100_1",
        "./data/fl_200_7",
        "./data/fl_500_7",
        "./data/fl_1000_2",
        "./data/fl_2000_2"
    ]

    for input in cachelist:
        print("Generating: {0}".format(input))
        facilities, customer = parse_input_from_file(input)
        newCaches = Facility_cache()
        newCaches.generate_all_cache(facilities,customer)
        save_cache(newCaches, str(len(facilities)) + "_" + str(len(customer)) + ".cache")

if __name__ == "__main__":
    #generate_caches()
    print(random.sample({0},1)[0])