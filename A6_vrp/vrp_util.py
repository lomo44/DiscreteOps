# utility function sets for vrp problem
from collections import namedtuple

Customer = namedtuple("Customer", ['index', 'demand', 'x', 'y'])


def parse_input_data_from_file(input_file):
    with open(input_file, 'r') as _file:
        return parse_input_data_from_string(_file.read())

def parse_input_data_from_string(input_data):
    lines = input_data.split('\n')

    parts = lines[0].split()
    customer_count = int(parts[0])
    vehicle_count = int(parts[1])
    vehicle_capacity = int(parts[2])
    customers = []
    for i in range(1, customer_count+1):
        line = lines[i]
        parts = line.split()
        customers.append(Customer(i-1, int(parts[0]), float(parts[1]), float(parts[2])))

    #the depot is always the first customer in the input
    depot = customers[0]
    return depot, vehicle_count, vehicle_capacity, customers

    