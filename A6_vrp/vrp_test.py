import unittest
from vrp_util import parse_input_data_from_file
from vrp_structs import vrp_solution
from vrp_cache import vrp_cache,length
import os
# unit test for vrp function

class test_vrp_util(unittest.TestCase):
    def setUp(self):
        self.problem_context = parse_input_data_from_file("./data/vrp_5_4_1")
    def test_parse_input_file(self):
        self.assertEqual(len(self.problem_context.customers),5)
        self.assertIsInstance(self.problem_context.vehicle_list, vrp_solution)
        self.assertEqual(self.problem_context.vehicle_list.vehicle_capacity, 10)
        self.assertEqual(self.problem_context.vehicle_list.vehicle_count, 4)
    
class test_vrp_cache(unittest.TestCase):
    def setUp(self):
        self.problem_context = parse_input_data_from_file("./data/vrp_5_4_1")
        self.cache = vrp_cache()
        self.cache.generate_cache(self.problem_context)
    def test_cache_size(self):
        self.assertEqual(len(self.cache.customer_to_customer_cache),5)
    def test_cache_accuracy(self):
        for customerA in self.problem_context.customers:
            for customerB in self.problem_context.customers:
                distance = length(customerA,customerB)
                self.assertAlmostEqual(distance, self.cache.get_distance_between_customers(customerA.index,customerB.index),msg="{0}-{1}".format(customerA.index, customerB.index), places=3)


class test_base(unittest.TestCase):
    def test_parsing_from_file(self):
        self.assertEqual(50, 50)


if __name__ == "__main__":
    unittest.main()
