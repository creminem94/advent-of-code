import os
import numpy as np

def part_1():
    with open(os.path.join(os.path.dirname(__file__), 'math.txt'), 'r') as file:
        # read lines
        content = file.read()
        lines = content.splitlines()
        n_lines = len(lines)
        tokens = np.array([list(map(int, line.split())) for line in lines[0:-1]])
        signs = list(lines[-1].split())
        print(signs)

        total = 0

        for i in range(len(signs)):
            if signs[i] == '+':
                total += np.sum(tokens[:, i])
            elif signs[i] == '*':
                total += np.prod(tokens[:, i])

        print(total)    


def part_2():
    with open(os.path.join(os.path.dirname(__file__), 'math.txt'), 'r') as file:
        # read lines
        content = file.read()
        lines = content.splitlines()
        char_array = np.array([list(line) for line in lines[0:-1]])
        
        idx = len(lines[0]) - 1
        elements = []
        total = 0
        while idx >= 0:
            col = ''.join(char_array[:, idx]).strip()
            sign = lines[-1][idx].strip()
            idx -= 1
            if col == '':
                continue
            elements.append(int(col))
            if sign != '':  
                current_value = np.sum(elements) if sign == '+' else np.prod(elements)
                total += current_value
                elements = []        
                continue

            
            

        print(total)


part_2()