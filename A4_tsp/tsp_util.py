import math
import pickle
from array import array
def distance_between_two_point(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

def generate_distance_dict(point_dict):
    distance_dict = []
    for start_index in range(0, len(point_dict)):
        print(start_index)
        newarray=array('f')
        for sub_index in range(start_index+1, len(point_dict)):
            newarray.append(distance_between_two_point(point_dict[start_index], point_dict[sub_index]))
        distance_dict.append(newarray)
    return distance_dict

def save_distance_dict(distance_dict, save_path):
    with open(save_path, 'wb') as f:
        pickle.dump(distance_dict, f, pickle.HIGHEST_PROTOCOL)

def load_distance_dict(load_path):
    with open(load_path, 'rb') as f:
        return pickle.load(f)