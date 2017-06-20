import math
from array import array
from vrp_structs import vrp_problem_context



def length(customer1, customer2):
    return math.sqrt((customer1.x - customer2.x)**2 + (customer1.y - customer2.y)**2)


class vrp_cache(object):
    def __init__(self):
        self.customer_to_customer_cache = []

    def generate_cache(self, problem_context:vrp_problem_context):
        for from_index in range(len(problem_context.customers)):
            cache_entry = array('f')
            for to_index in range(from_index,len(problem_context.customers)):
                cache_entry.append(
                    length(problem_context.customers[from_index], problem_context.customers[to_index]))
            self.customer_to_customer_cache.append(cache_entry)

    def get_distance_between_customers(self, customer_index_A, customer_index_B):
        if customer_index_A > customer_index_B:
            customer_index_A, customer_index_B = customer_index_B, customer_index_A
        if customer_index_A == customer_index_B:
            return 0
        else:
            return self.customer_to_customer_cache[customer_index_A][customer_index_B - customer_index_A]

    def get_distance_between_depot(self, customer_indexA):
        return self.customer_to_customer_cache[0][customer_indexA]
