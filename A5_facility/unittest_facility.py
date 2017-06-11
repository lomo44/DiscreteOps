
import unittest
import os
from A5_facility.facility_caching import *
from A5_facility.facility_util import *
class test_base(unittest.TestCase):
    def test_parsing_from_file(self):
        facilities,customers = parse_input_from_file("./data/fl_25_2")
        self.assertEqual(len(facilities),25)
        self.assertEqual(len(customers),50)
class test_order_cacheing(unittest.TestCase):
    def setUp(self):
        facilities, customers = parse_input_from_file("./data/fl_3_1")
        self.facilities = facilities
        self.customers = customers
        self.distance_cache = generate_distance_cache(self.facilities, self.customers)
        self.order_cache = generate_order_cache(self.distance_cache)
    def test_generate_order_cache_capacity(self):
        self.assertEqual(len(self.order_cache), len(self.customers))
    def test_generate_order_cache_accuracy(self):
        self.assertListEqual(list(self.order_cache[0]), [0, 1, 2])
        self.assertListEqual(list(self.order_cache[1]), [0, 1, 2])
        self.assertListEqual(list(self.order_cache[2]), [0, 1, 2])
        self.assertListEqual(list(self.order_cache[3]), [1, 0, 2])
    def test_save_generate_order_cache(self):
        save_distance_dict(self.order_cache, 'temp.ocache')
        self.assertTrue(os.path.exists('temp.ocache'))
        os.remove('temp.ocache')
    def test_load_generate_order_cache(self):
        save_distance_dict(self.order_cache, 'temp.ocache')
        cache = load_distance_dict('temp.ocache')
        self.assertEqual(len(cache), len(self.customers))
        self.assertListEqual(self.order_cache, cache)
        os.remove('temp.ocache')
class test_distance_caching(unittest.TestCase):
    def setUp(self):
        facilities, customers = parse_input_from_file("./data/fl_3_1")
        self.facilities = facilities
        self.customers = customers
        self.distance_cache = generate_distance_cache(self.facilities, self.customers)
        self.order_cache = generate_order_cache(self.distance_cache)
    def test_generate_distance_cache_accuracy(self):
        self.assertAlmostEqual(self.distance_cache[0][0], 469.5189, 3)
    def test_generate_distance_cache(self):
        self.assertEqual(len(self.distance_cache), len(self.customers))
    def test_save_generate_distance_cache(self):
        save_distance_dict(self.distance_cache, 'temp.dcache')
        self.assertTrue(os.path.exists('temp.dcache'))
        os.remove('temp.dcache')
    def test_load_generate_distance_cache(self):
        save_distance_dict(self.distance_cache, 'temp.dcache')
        cache = load_distance_dict('temp.dcache')
        self.assertEqual(len(cache), len(self.customers))
        self.assertListEqual(self.distance_cache, cache)
        os.remove('temp.dcache')
class test_util(unittest.TestCase):
    def setUp(self):
        facilities, customers = parse_input_from_file("./data/fl_3_1")
        self.facilities = facilities
        self.customers = customers
        self.distance_cache = generate_distance_cache(self.facilities, self.customers)
        self.order_cache = generate_order_cache(self.distance_cache)
    def test_get_nearest_unopened_facility(self):
        unopen = get_nearest_unopened_facility([],self.customers[0],self.order_cache,self.facilities)
        self.assertEqual(unopen,0)
        unopen = get_nearest_unopened_facility([0], self.customers[0], self.order_cache, self.facilities)
        self.assertEqual(unopen,1)
        unopen = get_nearest_unopened_facility([1,2], self.customers[0], self.order_cache, self.facilities)
        self.assertEqual(unopen, 0)
        unopen = get_nearest_unopened_facility([0,1,2], self.customers[0], self.order_cache, self.facilities)
        self.assertEqual(unopen, None)


if __name__ == "__main__":
    unittest.main()