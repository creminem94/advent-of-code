import os
from itertools import permutations
import numpy as np


def part_1():
    with open(os.path.join(os.path.dirname(__file__), 'factory.txt'), 'r') as file:
        # read lines
        content = file.read()
        lines = content.splitlines()
        #[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
        #[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
        #[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
        total = 0
        for line in lines:
            parts = line.split(' ')
            # transform the first part into ones and zeros
            objective = parts[0].replace('.', '0').replace('#', '1')[1:-1]
            buttons = parts[1:-1]
            
            # last part not needed for now
            # each button indicates which bits to flip
            best_sequence, best_score = find_best_sequence(objective, buttons)
            print(f"Objective: {objective}, Best sequence: {best_sequence}, Best score: {best_score}")
            total += best_score
        
        print(f"Total score: {total}")


def find_best_sequence(objective, buttons):
    # try all permutations of buttons, from length 1 to len(buttons)
    n = len(buttons)

    for r in range(1, n + 1):
        for perm in permutations(buttons, r):
            current = list('0' * len(objective))
            for button in perm:
                indices = list(map(int, button.strip('()').split(',')))
                for index in indices:
                    current[index] = '1' if current[index] == '0' else '0'
                # check if current matches objective
                if ''.join(current) == objective:
                    return perm, r
    return None, n + 1  # no sequence found
#part_1()

def part_2_old():
    with open(os.path.join(os.path.dirname(__file__), 'factory.txt'), 'r') as file:
        # read lines
        content = file.read()
        lines = content.splitlines()
        total = 0
        for line in lines:
            parts = line.split(' ')
            objective_sums = np.array(list(map(int, parts[-1][1:-1].split(','))), dtype=int)
            buttons = parts[1:-1]
            # sort buttons by number of indices they affect, descending
            buttons.sort(key=lambda x: -len(x.strip('()').split(',')))
            # convert buttons into vectors of zeros and ones on indeces they affect
            button_vectors = []
            for button in buttons:
                vector = np.zeros(len(objective_sums), dtype=int)
                indices = list(map(int, button.strip('()').split(',')))
                for index in indices:
                    vector[index] = 1
                button_vectors.append(vector)
            
            best_sequence, best_score = find_best_sum_sequence(objective_sums, button_vectors)
            print(f"Objective: {objective_sums}, Best sequence: {best_sequence}, Best score: {best_score}")
            total += best_score
        
        print(f"Total score: {total}")

def find_best_sum_sequence(objective_sums, buttons):
    # this in not efficient, let's use freaking math with Ax = b
    found = False
    current_sequence = []
    current_results = np.zeros(len(objective_sums), dtype=int)
    i = 0
    while not found:
        v = find_next_valid(objective_sums, buttons, current_results, i)
        if v is None:
            # backtrack, assume sequence will always 
            last_idx = current_sequence.pop()
            current_results = current_results - buttons[last_idx]
            i = last_idx + 1
            continue
        current_sequence.append(v)
        i = 0
        current_results = current_results + buttons[v]
        if np.array_equal(current_results, objective_sums):
            found = True
            break

    return current_sequence, len(current_sequence)
        
def find_next_valid(objective_sums, buttons, current_results, start_index=0):
    for i in range(start_index, len(buttons)):
        if test_button(objective_sums, buttons[i], current_results):
            return i
        
    return None

def test_button(objective_sums, button, current_results):
    return np.all(current_results + button <= objective_sums)
        
        
def part_2():
    # will solve in matlab
    with open(os.path.join(os.path.dirname(__file__), 'factory.txt'), 'r') as file:
        # read lines
        content = file.read()
        lines = content.splitlines()
        for line in lines:
            parts = line.split(' ')
            objective_sums = np.array(list(map(int, parts[-1][1:-1].split(','))), dtype=int)
            buttons = parts[1:-1]
            # convert buttons into vectors of zeros and ones on indeces they affect
            button_vectors = []
            for button in buttons:
                vector = np.zeros(len(objective_sums), dtype=int)
                indices = list(map(int, button.strip('()').split(',')))
                for index in indices:
                    vector[index] = 1
                button_vectors.append(vector)
            
            A = np.array(button_vectors).T
            b = objective_sums
            # Solve Ax = b in GF(2)
            
        

