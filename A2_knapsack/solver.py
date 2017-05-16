#!/usr/bin/python
# -*- coding: utf-8 -*-
from A2_knapsack.Node import TreeNode
import queue
import random
import math
import copy

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

upper_bound_cache_hit = 0
def tree(items ,capacity):


    taken, greedy_value = greedy(items,capacity)

    sorted_items = sorted(items, reverse=True, key=lambda x: x.density)
    potential_cache = []
    upper_bound_cache = {}
    potential_cache.append(sorted_items)

    for i in range(0,len(items)):
        sorted_items.remove(items[i])
        potential_cache.append(sorted_items[:])

    def get_upper_bound(index, sub_capacity):
        if index not in upper_bound_cache:
            upper_bound_cache[index] = {}
        if sub_capacity not in upper_bound_cache[index]:
            upper_bound_cache[index][sub_capacity] = -1
        if upper_bound_cache[index][sub_capacity] != -1:
            global upper_bound_cache_hit
            upper_bound_cache_hit = upper_bound_cache_hit+1
            return upper_bound_cache[index][sub_capacity]
        else:
            temp = sub_capacity
            upper_bound = 0
            for item in potential_cache[index]:
                if item.weight <= sub_capacity :
                    weight = min(item.weight, temp)
                    temp -= weight
                    upper_bound += weight * item.density
                    if temp == 0:
                        upper_bound_cache[index][sub_capacity] = upper_bound
                        return upper_bound
            upper_bound_cache[index][sub_capacity] = upper_bound
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
                #print("Node Count: ", nodeCount)
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
                nodeCount += 1
                #print("Node Count: ",nodeCount)
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

    print("Node Count: ", nodeCount)
    print("Upper Bound Cache Hits: ",upper_bound_cache_hit )
    return taken,bestValue

def tree2(items, capcity):
    # breath-first search
    #items = list(map(lambda x: Item(x.index,x.value,x.weight,x.density), items))
    taken, baseline_value = greedy(items, capcity)
    sorted_items = sorted(items, reverse=True, key=lambda x: x.density)
    #print("BaseLine: ",baseline_value)
    potential_cache = []
    upper_bound_cache = {}
    potential_cache.append(sorted_items[:])
    for i in range(0,len(items)):
        sorted_items.remove(items[i])
        potential_cache.append(sorted_items[:])
    def get_upper_bound(index, sub_capacity):
        if index not in upper_bound_cache:
            upper_bound_cache[index] = {}
        if sub_capacity not in upper_bound_cache[index]:
            upper_bound_cache[index][sub_capacity] = -1
        if upper_bound_cache[index][sub_capacity] != -1:
            global upper_bound_cache_hit
            upper_bound_cache_hit = upper_bound_cache_hit+1
            return upper_bound_cache[index][sub_capacity]
        else:
            temp = sub_capacity
            upper_bound = 0
            for item in potential_cache[index]:
                if item.weight <= sub_capacity:
                    weight = min(item.weight, temp)
                    temp -= weight
                    upper_bound += weight * item.density
                    if temp == 0:
                        upper_bound_cache[index][sub_capacity] = upper_bound
                        return upper_bound
            upper_bound_cache[index][sub_capacity] = upper_bound
            return upper_bound

    current_best = baseline_value
    current_best_node = None
    nodeQueue = queue.PriorityQueue()

    rootNode = TreeNode()
    rootNode.depth = 0
    rootNode.isRoot = True
    rootNode.value = 0
    rootNode.weight = capcity
    rootNode.potential=get_upper_bound(0,capcity)

    nodeQueue.put((1/rootNode.potential,rootNode))

    while nodeQueue.qsize() != 0:
        current_node = nodeQueue.get()[1]
        if current_node.potential > current_best:
            if current_node.left is None:
                target_weight = current_node.weight - items[current_node.depth].weight
                if target_weight >= 0:
                    target_value = current_node.value + items[current_node.depth].value
                    target_potential = get_upper_bound(current_node.depth+1, target_weight) + target_value
                    if target_potential > current_best:
                        newNode = TreeNode()
                        newNode.depth = current_node.depth + 1
                        newNode.potential = target_potential
                        newNode.value = target_value
                        newNode.weight = target_weight
                        newNode.parrent = current_node
                        current_node.left = newNode
                        if target_potential > target_value:
                            nodeQueue.put((1/newNode.potential,newNode))
                        if target_potential == target_value:
                            if target_value > current_best:
                                print("Current Best: {0}, depth: {1}".format(target_value,current_node.depth))
                                current_best = target_value
                                current_best_node = newNode
                pass
            if current_node.right is None:
                target_potential = get_upper_bound(current_node.depth+1, current_node.weight) + current_node.value
                if target_potential > current_best:
                    newNode = TreeNode()
                    newNode.depth = current_node.depth + 1
                    newNode.potential = target_potential
                    newNode.value = current_node.value
                    newNode.weight = current_node.weight
                    newNode.parrent = current_node
                    current_node.right = newNode
                    if target_potential > target_value:
                        nodeQueue.put((1 / newNode.potential, newNode))
                    if target_potential == target_value:
                        if target_value > current_best:
                            print("Current Best: {0}, depth: {1}".format(target_value, current_node.depth))
                            current_best = target_value
                            current_best_node = newNode

    result_capacity = 0
    if current_best != baseline_value:
        taken = [0] * len(items)
        while current_best_node.isRoot == False:
            parent = current_best_node.parrent
            if current_best_node == parent.left:
                taken[parent.depth] = 1
                result_capacity += items[parent.depth].weight
            current_best_node = parent

    return taken,current_best


def dp_1(items,capacity):
    sorted_items = sorted(items, key=lambda x:x.weight)
    min_weight = sorted_items[0].weight
    max_weight = sorted_items[-1].weight
    min_diff = sys.maxsize
    for index in range(1,len(sorted_items)-1):
        if sorted_items[index+1].weight - sorted_items[index].weight < min_diff:
           min_diff = sorted_items[index+1].weight - sorted_items[index].weight
    print("Min: {0}, Min: {1}, min_diff: {2}".format(min_weight,max_weight,min_diff))
    print("Capacity: {0}".format(capacity))
    finaltable = []
    # create zero table
    finaltable.append([0]*(capacity-min_weight+1))

    for index in range(1,len(items)+1):
        newvalues = []
        for sub_capacity in range(min_weight, capacity+1):
            if items[index-1].weight <= sub_capacity:
                gapweight = sub_capacity-items[index-1].weight
                gapvalue = 0
                if gapweight >= min_weight:
                    gapvalue = finaltable[index-1][gapweight-min_weight]
                bestvalue = max(finaltable[index-1][sub_capacity-min_weight], items[index-1].value + gapvalue)
                newvalues.append(bestvalue)
            else:
                newvalues.append(finaltable[index-1][sub_capacity-min_weight])
        finaltable.append(newvalues)
    #back tracking
    current_weight = capacity
    final_item = len(items)
    taken = []
    value = finaltable[final_item][current_weight-min_weight]
    while current_weight != 0 and final_item !=0:
        if finaltable[final_item][current_weight-min_weight] == finaltable[final_item-1][current_weight-min_weight]:
            taken = [0]+taken
            pass
        else:
            taken = [1]+taken
            current_weight -= items[final_item-1].weight
        final_item -=1
    while len(taken) != len(items):
        taken = [0] + taken

    return taken,value

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
        taken, value = dp_1(items, capacity)
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

