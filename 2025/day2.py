
import os

def part_1():
    total = 0

    with open(os.path.join(os.path.dirname(__file__), 'products.txt'), 'r') as file:
        content = file.read()
        ranges = content.split(',')
        for r in ranges:
            low, high = map(int, r.split('-'))
            if low > high:
                continue
            for i in range(low, high + 1):
                if len(str(i)) % 2 != 0:
                    continue
                s = str(i)
                s1 = s[:len(s)//2]
                s2 = s[len(s)//2:]
                if s1 == s2:
                    total += int(i)

    print(total)

def part_2():
    total = 0

    with open(os.path.join(os.path.dirname(__file__), 'products.txt'), 'r') as file:
        content = file.read()
        ranges = content.split(',')
        for r in ranges:
            low, high = map(int, r.split('-'))
            if low > high:
                continue
            for i in range(low, high + 1):
                total += parse_s(str(i))
                
                
    print(total)

def parse_s(s):
    max_len = len(s)/2
    for length in range(1, int(max_len) + 1):
        if test_len(s, length):
            return int(s)
    return 0

def test_len(s, length):
    # split s into chunks of length
    chunks = [s[i:i+length] for i in range(0, len(s), length)]
    # if all chunks are equal, return True
    return all(chunk == chunks[0] for chunk in chunks)

if __name__ == '__main__':
    part_2()