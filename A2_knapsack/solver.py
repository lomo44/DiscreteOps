#!/usr/bin/python
# -*- coding: utf-8 -*-
from Node import *

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight','density'])



def parseInputData(lines):
    # parse the input

    items = []

    for i in range(1, len(lines)-1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i - 1, int(parts[0]), int(parts[1]), float(int(parts[0])/int(parts[1]))))
    return items
def formOuputData(taken,value,checked=False):
    if checked:
        output_data = str(value) + ' ' + str(1) + '\n'
    else:
        output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data



def greedy(items,capacity):
    value = 0
    weight = 0
    taken = [0] * len(items)

    for item in items:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight

    return taken,value

def tree(items ,capacity):

    taken, greedy_value = greedy(items,capacity)

    def get_upper_bound(index, sub_capacity):

        sub_items = sorted(items[index:], reverse=True, key=lambda x: x.density)
        # for i in range(0,index):
        #     sub_items.remove(items[i])
        temp = sub_capacity
        upper_bound = 0
        for item in sub_items:
            if item.weight <= sub_capacity :
                weight = min(item.weight, temp)
                temp -= weight
                upper_bound += weight * item.density
                if temp == 0:
                    return upper_bound
        return upper_bound

    # sort items by weight

    bestPotential = get_upper_bound(0,capacity)

    rootNode = TreeNode()
    rootNode.depth = 0
    rootNode.potential = bestPotential
    rootNode.weight = capacity
    rootNode.value = 0
    rootNode.isRoot = True
    current_node = rootNode
    current_max = greedy_value
    total_item_count = len(items)
    current_leaf = None
    nodeCount = 0
    while current_node.isRoot!=True or current_node.left is None or current_node.right is None:
        if current_node.depth < total_item_count:
            if current_node.left is None:
                newNode = TreeNode()
                nodeCount+=1
                newNode.parrent = current_node
                current_node.left = newNode
                # creating left node
                current_node.left.weight = current_node.weight - items[current_node.depth].weight
                if current_node.left.weight >= 0:
                    current_node.left.isRoot = False
                    current_node.left.depth = current_node.depth+1
                    current_node.left.value = current_node.value + items[current_node.depth].value
                    current_node.left.potential = get_upper_bound(current_node.left.depth, current_node.left.weight) + current_node.left.value

                if current_node.left.weight >= 0 and current_node.left.potential > current_max:
                    if current_node.left.potential > current_node.left.value:
                        current_node = current_node.left
                    else:
                        if current_node.left.weight >= 0:
                            if current_node.left.potential > current_max:
                                current_max = current_node.left.potential
                                current_leaf = current_node.left
                else:
                    pass
            elif current_node.right is None:
                # populate right node
                newNode = TreeNode()
                newNode.parrent = current_node
                newNode.depth = current_node.depth + 1
                current_node.right = newNode
                current_node.right.value = current_node.value
                current_node.right.weight = current_node.weight
                current_node.right.depth = current_node.depth+1
                current_node.right.potential = get_upper_bound(current_node.right.depth,current_node.weight) + current_node.value
                if current_node.right.potential > current_max:
                    current_node = current_node.right
                else:
                    pass
            else:
                current_node = current_node.parrent
        else:
            if current_node.weight >= 0:
                if current_node.potential > current_max:
                    current_max = current_node.potential
                    current_leaf = current_node
            current_node = current_node.parrent
    # back tracking the data
    taken=[0]*total_item_count
    bestValue = current_leaf.value
    result_capacity = 0
    if bestValue != greedy_value:
        while current_leaf.isRoot == False:
            parent = current_leaf.parrent
            if current_leaf == parent.left:
                taken[parent.depth] = 1
                result_capacity += items[parent.depth].weight
            current_leaf = parent

    return taken,bestValue


def solve_it(input_data):
    # Modify this code to run your optimization algorithm
    lines = input_data.split('\n')
    firstLine = lines[0].split()
    capacity = int(firstLine[1])
    items = parseInputData(lines)

    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full

    base = False
    if base:
        taken,value = greedy(items, capacity)
    else:
        taken, value = tree(items, capacity)
    return formOuputData(taken, value, not base);
    #return formOuputData(taken, value, False);


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

