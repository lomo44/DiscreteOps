import math
import _pickle as cPickle
import marshal
from array import array
from collections import namedtuple

Point = namedtuple("Point", ['x', 'y'])
def distance_between_two_point(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

def generate_distance_dict(point_dict):
    distance_dict = []
    for start_index in range(0, len(point_dict)):
        print("Index: {0}".format(start_index))
        newarray=array('f')
        for sub_index in range(start_index+1, len(point_dict)):
            newarray.append(distance_between_two_point(point_dict[start_index], point_dict[sub_index]))
        distance_dict.append(newarray)
    return distance_dict

def save_distance_dict(distance_dict, save_path):
    with open(save_path, 'wb') as f:
        cPickle.dump(distance_dict, f)

def load_distance_dict(load_path):
    with open(load_path, 'rb') as f:
        return cPickle.load(f)

def get_distance_from_dict(p1_index, p2_index, distance_dict):
    if p1_index != p2_index:
        if p2_index > p1_index:
            return distance_dict[p1_index][p2_index-p1_index-1]
        if p1_index > p2_index:
            return distance_dict[p2_index][p1_index - p2_index - 1]
    return -1

def parse_data(input_data):
    lines = input_data.split('\n')
    nodeCount = int(lines[0])
    points = []
    for i in range(1, nodeCount + 1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))
    return points

def convert_point_list_to_dict(point_list):
    point_dict = {}
    for index in range(len(point_list)):
        point_dict[index] = point_list[index]
    return point_dict

def get_total_distance(solution, distance_dict):
    total_distance = 0
    for index in range(len(solution)-1):
        total_distance += get_distance_from_dict(solution[index], solution[index+1], distance_dict)
    total_distance += get_distance_from_dict(solution[len(solution)-1],solution[0],distance_dict)
    return total_distance

def generate_5_cache():
    with open('./data/tsp_5_1', 'r') as input_data_file:
        input_data = input_data_file.read()
        point_list = parse_data(input_data)
        point_dict = convert_point_list_to_dict(point_list)
        save_distance_dict(generate_distance_dict(point_dict), '5.cache')

def generate_51_cache():
    file_list = [
        "./data/tsp_5_1",
        "./data/tsp_51_1",
        "./data/tsp_100_3",
        "./data/tsp_200_2",
        "./data/tsp_574_1",
        "./data/tsp_1889_1",
        "./data/tsp_33810_1"
    ]
    for file in file_list:
        print("Generating {0}".format(file))
        with open(file, 'r') as input_data_file:
            input_data = input_data_file.read()
            point_list = parse_data(input_data)
            point_dict = convert_point_list_to_dict(point_list)
            save_distance_dict(generate_distance_dict(point_dict), str(len(point_dict))+'.cache')

if __name__ == "__main__":
    generate_51_cache()