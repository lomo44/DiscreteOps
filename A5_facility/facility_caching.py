from array import array
import math

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

class Facility_cache:
    def __init__(self):
        self.distance_cache = None
        self.distance_order_cache = None
        self.cost_cache = None
        self.cost_order_cache = None

    def generate_all_cache(self, facilities, customers):
        self.generate_distance_cache(facilities, customers)
        self.generate_cost_cache(facilities, customers)
        pass

    def generate_distance_cache(self, facilities, customers):
        self.distance_cache = []
        # distance matrix
        for customer in customers:
            distance_array = array('f')
            for faciility in facilities:
                distance_array.append(length(customer.location, faciility.location))
            self.distance_cache.append(distance_array)
        # distance order matrix
        self.distance_order_cache = []
        for entry in self.distance_cache:
            index_list = [i[0] for i in sorted(enumerate(entry), key=lambda x: x[1])]
            self.distance_order_cache.append(array('i', index_list))

    def generate_cost_cache(self, facilities, customers):
        self.cost_cache = []
        for customer in customers:
            cost_array = array('f')
            for facility in facilities:
                cost_array.append(length(customer.location, facility.location) + facility.setup_cost)
            self.cost_cache.append(cost_array)
        self.cost_order_cache = []
        for entry in self.cost_cache:
            index_list = [i[0] for i in sorted(enumerate(entry), key=lambda x: x[1])]
            self.cost_order_cache.append(array('i', index_list))

