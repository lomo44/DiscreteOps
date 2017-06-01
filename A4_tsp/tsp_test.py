import unittest
import os.path
from A4_tsp.tsp_util import *
from A4_tsp.tsp_solver import *
from A4_tsp.tsp_localsearch import *

class tests_tsp_util(unittest.TestCase):
    def setUp(self):
        with open('./data/tsp_51_1', 'r') as input_data_file:
            self.input_data = input_data_file.read()
            self.point_list = parse_data(self.input_data)
        self.point_dict = convert_point_list_to_dict(self.point_list)

    def test_parse_data(self):
        self.assertEqual(len(self.point_list),51)

    def test_convert_point_list_to_dict(self):
        self.assertEqual(len(self.point_list), len(self.point_dict))

    def test_generate_distant_dict(self):
        dict = generate_distance_dict(self.point_dict)
        self.assertEqual(len(dict),len(self.point_dict))

    def test_save_distant_dict(self):
        dict = generate_distance_dict(self.point_dict)
        save_distance_dict(dict, 'test.cache')
        self.assertTrue(os.path.exists('test.cache'))
        os.remove('test.cache')

    def test_load_distant_dict(self):
        dict = load_distance_dict('51.cache')
        self.assertTrue(len(dict) == len(self.point_dict))

    def test_load_distant_dict_functionality(self):
        dict = load_distance_dict('51.cache')
        distance = get_distance_from_dict(0,1,dict)
        self.assertAlmostEqual(20.223748416156685,distance,delta=5)
        distance = get_distance_from_dict(1,0,dict)
        self.assertAlmostEqual(20.223748416156685,distance,delta=5)
        distance = get_distance_from_dict(0,50, dict)
        self.assertAlmostEqual(36.05551275463989, distance, delta=5)
        distance = get_distance_from_dict(50,0, dict)
        self.assertAlmostEqual(36.05551275463989, distance, delta=5)

    def test_total_distance(self):
        solution = [0,1,2,3,4]
        distance_dict =  load_distance_dict('5.cache')
        self.assertEqual(get_total_distance(solution, distance_dict),4)
class tests_tsp_solver(unittest.TestCase):
    def setUp(self):
        with open('./data/tsp_51_1', 'r') as input_data_file:
            self.input_data = input_data_file.read()
            self.point_list = parse_data(self.input_data)
        self.point_dict = convert_point_list_to_dict(self.point_list)
        self.distance_dict = load_distance_dict(str(len(self.point_dict))+".cache")
    def test_51Point_Grade3(self):
        result, solution = tsp_master(self.point_dict, self.distance_dict)
        self.assertLess(result, 510)
    def test_51Point_Grade7(self):
        result, solution = tsp_master(self.point_dict, self.distance_dict)
        self.assertLess(result, 482)
    def test_51Point_Grade10(self):
        result, solution = tsp_master(self.point_dict, self.distance_dict)
        self.assertLess(result, 430)


class tests_tsp_local_search(unittest.TestCase):
    def setUp(self):
        with open('./data/tsp_5_1', 'r') as input_data_file:
            self.input_data = input_data_file.read()
            self.point_list = parse_data(self.input_data)
        self.point_dict = convert_point_list_to_dict(self.point_list)
        self.distance_dict = load_distance_dict(str(len(self.point_dict))+".cache")

    def test_2opt_operation(self):
        solution = [1,2,3,4,5]
        get_2opt(1,3,solution)
        self.assertListEqual(solution,[1,4,3,2,5])
        solution = [1,2,3,4,5]
        get_2opt(0,3,solution)
        self.assertListEqual(solution,[4,3,2,1,5])


    def test_2opt_reverse(self):
        solution = [1, 2, 3, 4, 5]
        get_2opt(3, 1, solution)
        self.assertListEqual(solution, [5,4, 3, 2, 1])
        solution = [1,2,3,4,5]
        get_2opt(3,0,solution)
        self.assertListEqual(solution, [4,2,3,1,5])
        solution = [1,2,3,4,5]
        get_2opt(2,0,solution)
        self.assertListEqual(solution, [3,2,1,5,4])
        solution = [1,2,3,4,5]
        get_2opt(4,2,solution)
        self.assertListEqual(solution, [2,1,5,4,3])

    def test_2opt_estimate_reverse_3size(self):
        solution = [0, 1, 2, 3, 4]
        test_difference = get_2opt_delta(3, 1, solution, self.distance_dict)
        previous_distance = get_total_distance(solution, self.distance_dict)
        get_2opt(3, 1, solution)
        current_distance = get_total_distance(solution, self.distance_dict)
        true_difference = previous_distance - current_distance
        self.assertEqual(true_difference, test_difference)

    def test_2opt_estimate_reverse_2size(self):
        solution = [0, 1, 2, 3, 4]
        test_difference = get_2opt_delta(2, 1, solution, self.distance_dict)
        previous_distance = get_total_distance(solution, self.distance_dict)
        get_2opt(2, 1, solution)
        current_distance = get_total_distance(solution, self.distance_dict)
        true_difference = previous_distance - current_distance
        self.assertEqual(true_difference, test_difference)

    def test_2opt_estimate_reverse_4size(self):
        solution = [0, 1, 2, 3, 4]
        test_difference = get_2opt_delta(3, 0, solution, self.distance_dict)
        previous_distance = get_total_distance(solution, self.distance_dict)
        get_2opt(3, 0, solution)
        current_distance = get_total_distance(solution, self.distance_dict)
        true_difference = previous_distance - current_distance
        self.assertEqual(true_difference, test_difference)

    def test_2opt_estimate_3size(self):
        solution = [0,1,2,3,4]
        test_difference = get_2opt_delta(1, 3, solution, self.distance_dict)
        previous_distance =  get_total_distance(solution,self.distance_dict)
        get_2opt(1,3,solution)
        current_distance = get_total_distance(solution,self.distance_dict)
        true_difference = previous_distance-current_distance
        self.assertEqual(true_difference,test_difference)

    def test_2opt_estimate_2size(self):
        solution = [0,1,2,3,4]
        test_difference = get_2opt_delta(1, 2, solution, self.distance_dict)
        previous_distance =  get_total_distance(solution,self.distance_dict)
        get_2opt(1,2,solution)
        current_distance = get_total_distance(solution,self.distance_dict)
        true_difference = previous_distance-current_distance
        self.assertEqual(true_difference,test_difference)

    def test_2opt_estimate_4size(self):
        solution = [0,1,2,3,4]
        test_difference = get_2opt_delta(1, 4, solution, self.distance_dict)
        previous_distance =  get_total_distance(solution,self.distance_dict)
        get_2opt(1,4,solution)
        current_distance = get_total_distance(solution,self.distance_dict)
        true_difference = previous_distance-current_distance
        self.assertEqual(true_difference,test_difference)


if __name__ == '__main__':
    unittest.main()