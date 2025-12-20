import os
import numpy as np

def part_1():
    with open(os.path.join(os.path.dirname(__file__), 'beam.txt'), 'r') as file:
        # read lines
        content = file.read()
        lines = content.splitlines()
        initial_pos = lines[0].index('S')
        beam_positions = set()
        beam_positions.add(initial_pos)
        total_splitter = 0
        for i in range(2, len(lines), 2):
            line = lines[i]
            beam_positions, splits = split(beam_positions, line)
            total_splitter += splits
            # print(f'After line {i//2}: {beam_positions}, total: {total_splitter}')

        print(total_splitter)

def split(beam_positions, line):
    new_positions = set()
    splits = 0
    for pos in beam_positions:
        if line[pos] == '^':
            new_positions.add(pos-1)
            new_positions.add(pos+1)
            splits += 1
        else:
            new_positions.add(pos)

    return new_positions, splits

def path_discovery(initial_pos, lines, i, side = 'L'):
    if i >= len(lines):
        return [[initial_pos]]
    # path = [initial_pos]
    sub_paths = []
    current_pos = initial_pos
    # for i in range(2, len(lines), 2):
    line = lines[i]
    if line[current_pos] == '^':
        if side == 'L':
            current_pos -= 1
        else:
            current_pos += 1
        left_paths = path_discovery(current_pos, lines, i+2, 'L')
        # map each path by prepending current_pos
        left_paths = map(lambda x: [initial_pos] + x, left_paths)
        sub_paths += left_paths
        right_paths = path_discovery(current_pos, lines, i+2, 'R')
        right_paths = map(lambda x: [initial_pos] + x, right_paths)
        sub_paths += right_paths
    # path.append(current_pos)
    else:
        middle_paths = path_discovery(current_pos, lines, i+2, side)
        middle_paths = map(lambda x: [initial_pos] + x, middle_paths)
        sub_paths += middle_paths

    return sub_paths

def part_2():
    with open(os.path.join(os.path.dirname(__file__), 'beam.txt'), 'r') as file:
        # read lines
        content = file.read()
        lines = content.splitlines()
        initial_pos = lines[0].index('S')
        # beam_positions = set()
        # beam_positions.add(initial_pos)
        # sub_left = path_discovery(initial_pos, lines, 2, side='L')
        # sub_right = path_discovery(initial_pos, lines, 2, side='R')
        # all_paths = sub_left + sub_right
        # # remove duplicates
        # all_paths = set(tuple(p) for p in all_paths)
        # print(len(all_paths))
        cache = {}
        total_paths = count_sub(initial_pos, lines, 2, cache)
        print(total_paths)

def count_sub(initial_pos, lines, i, cache):
    key = (initial_pos, i)
    if key in cache:
        return cache[key]
    if i >= len(lines):
        return 1
    total_paths = 0
    current_pos = initial_pos
    line = lines[i]
    if line[current_pos] == '^':
        
        # if current_pos < 2 or line[current_pos-2] != '^':
            # avoid taking the same path twice
        total_paths += count_sub(current_pos-1, lines, i+2, cache)
        total_paths += count_sub(current_pos+1, lines, i+2, cache)
    else:
        total_paths += count_sub(current_pos, lines, i+2, cache)

    cache[key] = total_paths
    return total_paths



part_2()