from copy import deepcopy
import unittest
import os
from facility_localsearch import *
from facility_util import *
from facility_solver import *
class test_base(unittest.TestCase):
    def test_parsing_from_file(self):
        facilities,customers = parse_input_from_file("./data/fl_25_2")
        self.assertEqual(len(facilities),25)
        self.assertEqual(len(customers),50)

class test_distance_caching(unittest.TestCase):
    def setUp(self):
        facilities, customers = parse_input_from_file("./data/fl_3_1")
        self.facilities = facilities
        self.customers = customers
        self.caches = Facility_cache()
        self.caches.generate_all_cache(self.facilities, self.customers)
        self.save_cache_name = 'temp.dcache'
    def test_generate_distance_cache_accuracy(self):
        self.assertAlmostEqual(self.caches.distance_cache[0][0], 469.5189, 3)
    def test_generate_distance_cache(self):
        self.assertEqual(len(self.caches.distance_cache), len(self.customers))
        self.assertEqual(len(self.caches.distance_order_cache), len(self.customers))
    def test_save_generate_distance_cache(self):
        save_cache(self.caches, self.save_cache_name)
        self.assertTrue(os.path.exists(self.save_cache_name))
        os.remove(self.save_cache_name)
    def test_load_generate_distance_cache(self):
        save_cache(self.caches,self.save_cache_name)
        cache = load_cache(self.save_cache_name)
        self.assertEqual(len(cache.distance_cache), len(self.customers))
        self.assertListEqual(self.caches.distance_cache, cache.distance_cache)
        self.assertListEqual(self.caches.distance_order_cache, cache.distance_order_cache)
        self.assertListEqual(self.caches.cost_cache, cache.cost_cache)
        self.assertListEqual(self.caches.cost_order_cache, cache.cost_order_cache)
        os.remove(self.save_cache_name)
    def test_generate_distance_order_cache_accuracy(self):
        self.assertListEqual(list(self.caches.distance_order_cache[0]), [0, 1, 2])
        self.assertListEqual(list(self.caches.distance_order_cache[1]), [0, 1, 2])
        self.assertListEqual(list(self.caches.distance_order_cache[2]), [0, 1, 2])
        self.assertListEqual(list(self.caches.distance_order_cache[3]), [1, 0, 2])
    def test_generate_cost_cache_size(self):
        self.assertEqual(len(self.caches.cost_cache), len(self.customers))
        self.assertEqual(len(self.caches.cost_order_cache), len(self.customers))
    def test_geneerate_cost_cache_accuracy(self):
        self.assertAlmostEqual(self.caches.cost_cache[0][0], self.caches.distance_cache[0][0]+self.facilities[0].setup_cost,3)
class test_util(unittest.TestCase):
    def setUp(self):
        facilities, customers = parse_input_from_file("./data/fl_3_1")
        self.facilities = facilities
        self.customers = customers
        self.caches = Facility_cache()
        self.caches.generate_all_cache(self.facilities, self.customers)
    def test_get_nearest_unopened_facility(self):
        unopen = get_nearest_facility(self.customers[0],self.facilities,[],self.caches)
        self.assertEqual(unopen,0)
        unopen = get_nearest_facility(self.customers[0],self.facilities,[0],self.caches)
        self.assertEqual(unopen,1)
        unopen = get_nearest_facility(self.customers[0],self.facilities,[1,2],self.caches)
        self.assertEqual(unopen, 0)
        unopen = get_nearest_facility(self.customers[0],self.facilities,[0,1,2],self.caches)
        self.assertEqual(unopen, None)
    def test_get_cost_and_capacity(self):
        cost = facility_greedy(deepcopy(self.facilities),self.customers,self.caches)
        self.assertAlmostEqual(cost, get_cost_and_capacity(deepcopy(self.facilities),self.customers,self.caches),3)
class test_localsearch(unittest.TestCase):
    def setUp(self):
        facilities, customers = parse_input_from_file("./data/fl_16_1")
        self.facilities = facilities
        self.customers = customers
        self.greedy_facilities = deepcopy(facilities)
        self.greedy_customer = deepcopy(customers)

        self.caches = Facility_cache()
        self.caches.generate_all_cache(self.facilities, self.customers)
        self.greedyCost = facility_greedy(self.greedy_facilities,self.greedy_customer,self.caches)
    def test_facility_reassign(self):
        for x in range(0,10):
            opened_facility_index = get_opened_facilities(self.greedy_customer)
            delta_cost, facility_changes, customer_changes = facility_reassign(self.greedy_facilities,
                                                                               self.greedy_customer, 1, self.caches,
                                                                               opened_facility_index)
            new_customers = deepcopy(self.greedy_customer)
            new_facilities = deepcopy(self.facilities)
            for customer in customer_changes:
                new_customers[customer].assigned_facility = customer_changes[customer][1]
            newcost = get_cost_and_capacity(new_facilities, new_customers, self.caches)
            self.assertAlmostEqual(newcost - self.greedyCost, delta_cost, places=1)
            new_diff_dict = {}
            for facility in new_facilities:
                if facility.capacity - self.greedy_facilities[facility.index].capacity != 0:
                    new_diff_dict[facility.index] = facility.capacity - self.greedy_facilities[facility.index].capacity
            self.assertDictEqual(facility_changes, new_diff_dict)

if __name__ == "__main__":
    unittest.main()