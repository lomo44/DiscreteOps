import unittest
from A6_vrp.vrp_util import *
import os
# unit test for vrp function
class test_vrp_util(unittest.TestCase):
    def test_parse_input_file(self):
        print(os.getcwd())
        parse_input_data_from_file("./data/vrp_5_4_2")
        
class test_base(unittest.TestCase):
    def test_parsing_from_file(self):
        self.assertEqual(50,50)
if __name__ == "__main__":
    unittest.main()