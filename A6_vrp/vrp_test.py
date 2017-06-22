import unittest
from vrp_util import parse_input_data_from_file, check_solution_valid, get_solution_cost
from vrp_cache import vrp_cache, length
from vrp_localsearch import vrp_local_search_context, vrp_local_search_type
from vrp_solver import vrp_greedy
import os


# unit test for vrp function

class test_vrp_util(unittest.TestCase):
    def setUp(self):
        self.problem_context = parse_input_data_from_file("./data/vrp_5_4_1")

    def test_parse_input_file(self):
        self.assertEqual(len(self.problem_context.customers), 5)
        self.assertEqual(self.problem_context.vehicle_max_capacity, 10)
        self.assertEqual(self.problem_context.vehicle_count, 4)


class test_vrp_cache(unittest.TestCase):
    def setUp(self):
        self.problem_context = parse_input_data_from_file("./data/vrp_5_4_1")
        self.cache = vrp_cache()
        self.cache.generate_cache(self.problem_context)

    def test_cache_size(self):
        self.assertEqual(len(self.cache.customer_to_customer_cache), 5)

    def test_cache_accuracy(self):
        for customerA in self.problem_context.customers:
            for customerB in self.problem_context.customers:
                distance = length(customerA, customerB)
                self.assertAlmostEqual(distance,
                                       self.cache.get_distance_between_customers(customerA.index, customerB.index),
                                       msg="{0}-{1}".format(customerA.index, customerB.index), places=3)

class test_vrp_local_search_small(unittest.TestCase):
    def setUp(self):
        self.problem_context = parse_input_data_from_file("./data/vrp_5_4_1")
        self.cache = vrp_cache()
        self.cache.generate_cache(self.problem_context)
        self.greedy_solution = vrp_greedy(self.problem_context, self.cache)

    def test_greedy_solution(self):
        self.assertTrue(check_solution_valid(self.problem_context, self.greedy_solution))
        self.assertEqual(self.greedy_solution.current_cost,
                         get_solution_cost(self.problem_context, self.greedy_solution, self.cache))

    def test_swap(self):
        for i in range(100):
            swap_context = vrp_local_search_context(vrp_local_search_type.vrp_swap)
            current_cost = self.greedy_solution.current_cost
            swap_context.get_estimate(self.greedy_solution, self.problem_context, self.cache)
            swap_context.apply_changes(self.greedy_solution, self.problem_context)

            self.assertTrue(check_solution_valid(self.problem_context, self.greedy_solution))
            self.assertEqual(self.greedy_solution.current_cost - current_cost, swap_context.cost_delta)
            self.assertEqual(get_solution_cost(self.problem_context, self.greedy_solution, self.cache),self.greedy_solution.current_cost)

    def test_move(self):
        for i in range(100):
            move_context = vrp_local_search_context(vrp_local_search_type.vrp_move)
            current_cost = self.greedy_solution.current_cost
            move_context.get_estimate(self.greedy_solution, self.problem_context, self.cache)
            move_context.apply_changes(self.greedy_solution, self.problem_context)
            self.assertTrue(check_solution_valid(self.problem_context, self.greedy_solution), "Solution is Not valid")
            self.assertEqual(self.greedy_solution.current_cost - current_cost, move_context.cost_delta)
            self.assertEqual(get_solution_cost(self.problem_context, self.greedy_solution, self.cache),self.greedy_solution.current_cost)

    def test_trade(self):
        for i in range(100):
            move_context = vrp_local_search_context(vrp_local_search_type.vrp_trade)
            current_cost = self.greedy_solution.current_cost
            move_context.get_estimate(self.greedy_solution, self.problem_context, self.cache)
            move_context.apply_changes(self.greedy_solution, self.problem_context)
            self.assertTrue(check_solution_valid(self.problem_context, self.greedy_solution), "Solution is Not valid")
            self.assertEqual(self.greedy_solution.current_cost - current_cost, move_context.cost_delta)
            self.assertEqual(get_solution_cost(self.problem_context, self.greedy_solution, self.cache),
                             self.greedy_solution.current_cost)
class test_vrp_local_search_big(unittest.TestCase):
    def setUp(self):
        self.problem_context = parse_input_data_from_file("./data/vrp_481_38_1")
        self.cache = vrp_cache()
        self.cache.generate_cache(self.problem_context)
        self.greedy_solution = vrp_greedy(self.problem_context, self.cache)

    def test_greedy_solution(self):
        self.assertTrue(check_solution_valid(self.problem_context, self.greedy_solution))
        self.assertEqual(self.greedy_solution.current_cost,
                         get_solution_cost(self.problem_context, self.greedy_solution, self.cache))

    def test_swap(self):
        for i in range(100):
            swap_context = vrp_local_search_context(vrp_local_search_type.vrp_swap)
            current_cost = self.greedy_solution.current_cost
            swap_context.get_estimate(self.greedy_solution, self.problem_context, self.cache)
            swap_context.apply_changes(self.greedy_solution, self.problem_context)

            self.assertTrue(check_solution_valid(self.problem_context, self.greedy_solution))
            self.assertEqual(self.greedy_solution.current_cost - current_cost, swap_context.cost_delta)
            self.assertEqual(get_solution_cost(self.problem_context, self.greedy_solution, self.cache),self.greedy_solution.current_cost)

    def test_move(self):
        for i in range(100):
            move_context = vrp_local_search_context(vrp_local_search_type.vrp_move)
            current_cost = self.greedy_solution.current_cost
            move_context.get_estimate(self.greedy_solution, self.problem_context, self.cache)
            move_context.apply_changes(self.greedy_solution, self.problem_context)
            self.assertTrue(check_solution_valid(self.problem_context, self.greedy_solution), "Solution is Not valid")
            self.assertEqual(self.greedy_solution.current_cost - current_cost, move_context.cost_delta)
            self.assertEqual(get_solution_cost(self.problem_context, self.greedy_solution, self.cache),self.greedy_solution.current_cost)

    def test_trade(self):
        for i in range(100):
            move_context = vrp_local_search_context(vrp_local_search_type.vrp_trade)
            current_cost = self.greedy_solution.current_cost
            move_context.get_estimate(self.greedy_solution, self.problem_context, self.cache)
            move_context.apply_changes(self.greedy_solution, self.problem_context)
            self.assertTrue(check_solution_valid(self.problem_context, self.greedy_solution), "Solution is Not valid")
            self.assertEqual(self.greedy_solution.current_cost - current_cost, move_context.cost_delta)
            self.assertEqual(get_solution_cost(self.problem_context, self.greedy_solution, self.cache),
                                 self.greedy_solution.current_cost)



class test_base(unittest.TestCase):
    def test_parsing_from_file(self):
        self.assertEqual(50, 50)


if __name__ == "__main__":
    unittest.main()
