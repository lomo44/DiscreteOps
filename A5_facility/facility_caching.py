from collections import namedtuple
from array import array
import math
import os
import _pickle as cPickle
from A5_facility.facility_structs import *
Point = namedtuple("Point", ['x', 'y'])
#Facility = namedtuple("Facility", ['index', 'setup_cost', 'capacity', 'location'])
#Customer = namedtuple("Customer", ['index', 'demand', 'location', 'assigned_facility'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def parse_input_from_file(in_filePath):
    with open(in_filePath, 'r') as input_data_file:
        input_data = input_data_file.read()
        return parse_input_from_string(input_data)

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

def generate_distance_cache(facilities, customers):
    distance_list = []
    for customer in customers:
        distance_array = array('f')
        for faciility in facilities:
            distance_array.append(length(customer.location, faciility.location))
        distance_list.append(distance_array)
    return distance_list

def generate_order_cache(distance_list):
    order_list = []
    for customer in distance_list:
        index_list = [i[0] for i in sorted(enumerate(customer), key=lambda x:x[1])]
        order_list.append(array('i',index_list))
    return order_list

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
        distance_matrix = generate_distance_cache(facilities,customer)
        save_distance_dict(distance_matrix,str(len(facilities))+"_"+str(len(customer))+".dcache")
        order_matrix = generate_order_cache(distance_matrix)
        save_distance_dict(order_matrix,str(len(facilities))+"_"+str(len(customer))+".ocache")

def save_distance_dict(distance_dict, save_path):
    with open(save_path, 'wb') as f:
        cPickle.dump(distance_dict, f)

def load_distance_dict(load_path):
    with open(load_path, 'rb') as f:
        return cPickle.load(f)

def load_caches(facilities, customers):
    distance_cache_name = str(len(facilities))+"_"+str(len(customers))+".dcache"
    order_cache_name = str(len(facilities))+"_"+str(len(customers))+".ocache"
    distance_cache = None
    order_cache = None
    if os.path.exists(distance_cache_name):
        distance_cache = load_distance_dict(distance_cache_name)
    if os.path.exists(order_cache_name):
        order_cache = load_distance_dict(order_cache_name)
    return distance_cache,order_cache

def get_distance_from_dict(facility, customer, distance_dict):
    return distance_dict[customer.index][facility.index]



if __name__ == "__main__":
    generate_caches()