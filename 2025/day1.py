import os

pos = 50 # between 0 and 99
print(f'Initial position: {pos}')

zero_count = 0
#After L673: position 0, zero_count 5979
#After L92: position 8, zero_count 5980

with open(os.path.join(os.path.dirname(__file__), 'data.txt'), 'r') as file:
    content = file.read()
    # read each line
    lines = content.splitlines()
    for line in lines:
        direction = line[0]
        value = int(line[1:])
        n_zero = value // 100
        value = value % 100
        if direction == 'R':
            pos += value
            n_zero += pos // 100
        elif direction == 'L':
            old_pos = pos
            pos -= value
            if old_pos != 0:
                n_zero += - (pos // 100)
            if pos == 0 and value > 0 :
                n_zero += 1
        
        pos = pos % 100
        zero_count += n_zero
        print(f'After {line}: position {pos}, zero_count {zero_count}')

    
print(zero_count)