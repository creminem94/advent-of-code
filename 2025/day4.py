import os
import numpy as np

def part_1():

    with open(os.path.join(os.path.dirname(__file__), 'rolls.txt'), 'r') as file:
        # read lines
        content = file.read()
        lines = content.splitlines()
        total = exec(lines, add_zeros=True)

        print(total)

def part_2():
    with open(os.path.join(os.path.dirname(__file__), 'rolls.txt'), 'r') as file:
        # read lines
        content = file.read()
        lines = content.splitlines()
        total = 0
        while True:
            count = exec(lines, add_zeros=True, extract=True)
            if count == 0:
                break
            total += count

        print(total)


def exec(lines, add_zeros = False, extract = False):
    total = 0
    # add one line of zeros at start and end
    if add_zeros:
        lines.insert(0, '0' * len(lines[0]))
        lines.append('0' * len(lines[0]))
    for y in range(1, len(lines) - 1):
        # add zero at start and end of each line
        if y == 1 and add_zeros:
            lines[y-1] = '0' + lines[y-1] + '0'
            lines[y] = '0' + lines[y] + '0'

        if add_zeros:
            lines[y+1] = '0' + lines[y+1] + '0'
        for x in range(1, len(lines[y]) - 1):
            el = lines[y][x]
            if (el == '0'):
                continue
            
            # create a sub matrix around (x, y) of 3x3
            sub_matrix = [
                [int(x) for x in lines[y-1][x-1:x+2]],
                [int(x) for x in lines[y][x-1:x+2]],
                [int(x) for x in lines[y+1][x-1:x+2]]
            ]

            s = np.array(sub_matrix, dtype=int).sum()
            if s <= 4:
                total += 1
                if extract:
                    lines[y] = lines[y][:x] + '0' + lines[y][x+1:]

    return total
                

if __name__ == '__main__':
    part_2()