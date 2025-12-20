import os

max_digits = 12

def part_1():
    total = 0

    with open(os.path.join(os.path.dirname(__file__), 'batteries.txt'), 'r') as file:
        # read lines
        content = file.read()
        lines = content.splitlines()
        for line in lines:
            total += parseLine(line)

    print(total)

def parseLine(s):
    global max_digits
    jolt = ''
    for i in range(0, max_digits):
        high, s = getHighest(s, max_digits - i - 1)
        jolt += high
    print(f'Jolt string: {jolt}')
    return int(jolt)

def getHighest(s, skip_end = 1):
    # get the highest digit in s from the start to len(s) - skip_end
    # return the digit and the string after that digit
    to_check = s[:-skip_end] if skip_end > 0 else s
    max_digit = max(to_check)
    index = s.index(max_digit)
    return max_digit, s[index + 1:]

if __name__ == '__main__':
    part_1()