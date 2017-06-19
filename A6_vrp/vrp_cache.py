import math
from array import array

def length(customer1, customer2):
    return math.sqrt((customer1.x - customer2.x)**2 + (customer1.y - customer2.y)**2)

class vrp_cache(object):
    def __init__(self):
        self.customer_to_customer_cache = []
        self.depot_to_customer_cache = array('f')
    def generate_cache(self, customers, depot):
        for from_index in range(len(customers)):
            cache_entry = array('f')
            for to_index in range(from_index+1, len(customers)):
                cache_entry.append(length(customers[from_index],customers[to_index]))
            self.customer_to_customer_cache.append(cache_entry)
            self.depot_to_customer_cache.append(length(depot, customers(from_index)))
        
    def get_distance_between_customers(self, customer_index_A,customer_index_B):
        if customer_index_A > customer_index_B:
            customer_index_A, customer_index_B = customer_index_B, customer_index_A
        return self.customer_to_customer_cache[customer_index_A][customer_index_A-customer_index_B-1]
    
    def get_distance_between_depot(self, customer_indexA):
        return self.depot_to_customer_cache[customer_indexA]