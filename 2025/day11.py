import os
import numpy as np

class Node:
    def __init__(self, name, parents=[]):
        self.name = name
        self.children = []
        self.parents = parents

    

    
def part_1():
    with open(os.path.join(os.path.dirname(__file__), 'conns.txt'), 'r') as file:
        # read lines
        content = file.read()
        lines = content.splitlines()
        nodes = {}
        initial_node = None
        for line in lines:
            parts = line.split(': ')
            parent = parts[0]
            children = parts[1].split(' ')
            if parent not in nodes:
                nodes[parent] = Node(parent)
            if parent == 'you':
                initial_node = nodes[parent]
            for child in children:
                if child not in nodes:
                    nodes[child] = Node(child)
                nodes[parent].children.append(nodes[child])

        print(f"Total paths: {get_number_of_paths(initial_node)}")

    
def get_number_of_paths(initial_node):
    if len(initial_node.children) == 0:
        return 1
    total_paths = 0
    for child in initial_node.children:
        total_paths += get_number_of_paths(child)
    return total_paths

# part_1()
computed_paths = {}

def part_2():
    with open(os.path.join(os.path.dirname(__file__), 'conns.txt'), 'r') as file:
        # read lines
        content = file.read()
        lines = content.splitlines()
        nodes = {}
        svr_node = None
        dac_node = None
        fft_node = None
        out_node = None
        for line in lines:
            parts = line.split(': ')
            parent = parts[0]
            children = parts[1].split(' ')
            if parent not in nodes:
                nodes[parent] = Node(parent)
            if parent == 'svr':
                svr_node = nodes[parent]
            if parent == 'dac':
                dac_node = nodes[parent]
            if parent == 'fft':
                fft_node = nodes[parent]
            for child in children:
                if child not in nodes:
                    nodes[child] = Node(child, [nodes[parent]])
                if child == 'out' and out_node is None:
                    out_node = nodes[child]
                else:
                    nodes[child].parents.append(nodes[parent])
                nodes[parent].children.append(nodes[child])
    
        svr_to_dac = get_number_of_paths_to_node(svr_node, dac_node)
        dac_to_fft = get_number_of_paths_to_node(dac_node, fft_node)
        fft_to_out = get_number_of_paths_to_node(fft_node, out_node)
        svr_to_fft = get_number_of_paths_to_node(svr_node, fft_node)
        fft_to_dac = get_number_of_paths_to_node(fft_node, dac_node)
        dac_to_out = get_number_of_paths_to_node(dac_node, out_node)

        total_paths = svr_to_dac * dac_to_fft * fft_to_out + svr_to_fft * fft_to_dac * dac_to_out
        print(f"Total paths from svr to fft via dac: {total_paths}")

        
def get_number_of_paths_to_node(initial_node, target_node):
    if (initial_node.name, target_node.name) in computed_paths:
        return computed_paths[(initial_node.name, target_node.name)]
    print(f"Computing paths from {initial_node.name} to {target_node.name}")
    if initial_node == target_node:
        computed_paths[(initial_node.name, target_node.name)] = 1
        return 1
    if len(initial_node.children) == 0:
        computed_paths[(initial_node.name, target_node.name)] = 0
        return 0
    total_paths = 0
    for child in initial_node.children:
        total_paths += get_number_of_paths_to_node(child, target_node)
    computed_paths[(initial_node.name, target_node.name)] = total_paths
    return total_paths


part_2()