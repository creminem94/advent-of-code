import os
import numpy as np

def part_1():
    with open(os.path.join(os.path.dirname(__file__), 'ingredients.txt'), 'r') as file:
        # read lines
        content = file.read()
        ranges, ids = content.split('\n\n')
        range_values = []
        for r in ranges.splitlines():
            low, high = map(int, r.split('-'))
            range_values.append((low, high))

        total = 0
        for line in ids.splitlines():
            num_id = int(line)
            if search_valid(num_id, range_values):
                total += 1

        print(total)

def search_valid(num_id, range_values):
    # return also the index if found
    for i in range(len(range_values)):
        low, high = range_values[i]
        if num_id >= low and num_id <= high:
            # print(f'Valid ID: {num_id} in range {low}-{high}')
            return True, i
    return False, -1

def search_range_to_extend(low, high, range_values):
    for i in range(len(range_values)):
        r_low, r_high = range_values[i]
        if low <= r_low and high >= r_high:
            return True, i
    return False, -1

def find_spot(val, range_vector, test_equal=True):
    for i in range(0, len(range_vector)):
        if test_equal and val <= range_vector[i]:
            return i
        elif not test_equal and val < range_vector[i]:
            return i
    return len(range_vector)

def put_in_ranges(in_low, in_high, range_vector):
    if len(range_vector) == 0:
        range_vector.append(in_low)
        range_vector.append(in_high)
        return
    
    idx_low = find_spot(in_low, range_vector)

    # simple case, add to bottom
    if idx_low == len(range_vector):
        range_vector.append(in_low)
        range_vector.append(in_high)
        return
    
    idx_high = find_spot(in_high, range_vector, test_equal=False)

    if idx_low % 2 == 0:
        if idx_low != idx_high:
            range_vector[idx_low] = in_low
        else:
            range_vector.insert(idx_low, in_low)

    if idx_high != idx_low:
        to_del_start = idx_low+1 if idx_low % 2 == 0 else idx_low
        # to_del_end = idx_high - 1 if idx_high % 2 == 0 else idx_high
        to_del_end = idx_high 
        del range_vector[to_del_start:to_del_end]

    if idx_high % 2 == 0:
        range_vector.insert(idx_low + 1 if idx_low % 2 == 0 else idx_low, in_high)
    

def put_in_ranges_old(in_low, in_high, range_values):
    # we make sure that ranges are ordered
    if len(range_values) == 0:
        range_values.append((in_low, in_high))
        return
    
    idx_to_insert = -1
    idx_to_remove = []
    put = False

    for i in range(len(range_values)):
        low, high = range_values[i]
        if in_low < low and in_high < low:
            # insert before
            range_values.insert(i, (in_low, in_high))
            put = True
            return
        
        if in_low < low and in_high >= low and in_high <= high:
            # extend the low side
            range_values[i] = (in_low, high)
            put = True
            return
        
        if in_low < low and in_high > high:
            # extend to cover the whole range
            idx_to_insert = i
            idx_to_remove.insert(0, i)
            continue

        if in_low > high:
            # continue searching
            idx_to_insert = i + 1
            continue

        if in_low >= low and in_low <= high and in_high > high:
            # extend the high side
            range_values[i] = (low, in_high)
            put = True
            continue

    for idx in idx_to_remove:
        del range_values[idx]
    if idx_to_insert != -1 and not put:
        range_values.insert(idx_to_insert, (in_low, in_high))
        return
    


def part_2():
    with open(os.path.join(os.path.dirname(__file__), 'ingredients.txt'), 'r') as file:
        # read lines
        content = file.read()
        ranges, _ = content.split('\n\n')
        # even elemnets are lows, odd elements are highs
        range_vector = []
        for r in ranges.splitlines():
            low, high = map(int, r.split('-'))
            put_in_ranges(low, high, range_vector)

        total = 0
        for i in range(0, len(range_vector), 2):
            low = range_vector[i]
            high = range_vector[i+1]
            print(f'Range: {low}-{high}')
            total += (high - low + 1)

        print(total)
                

def part_2_old():
    with open(os.path.join(os.path.dirname(__file__), 'ing_test.txt'), 'r') as file:
        # read lines
        content = file.read()
        ranges, _ = content.split('\n\n')
        range_values = []
        for r in ranges.splitlines():
            low, high = map(int, r.split('-'))
            min_included, min_range_idx = search_valid(low, range_values)
            max_included, max_range_idx = search_valid(high, range_values)
            if min_included and max_included and min_range_idx == max_range_idx:
                continue

            if min_included and max_included:
                # two different ranges, merge them
                low1, high1 = range_values[min_range_idx]
                low2, high2 = range_values[max_range_idx]
                new_low = min(low1, low2)
                new_high = max(high1, high2)
                range_values[min_range_idx] = (new_low, new_high)
                del range_values[max_range_idx]
                r -= 1
                continue
            
            if min_included and not max_included:
                # extend the range at min_range_idx
                low1, high1 = range_values[min_range_idx]
                range_values[min_range_idx] = (low1, high)
                continue

            if not min_included and max_included:
                # extend the range at max_range_idx
                low1, high1 = range_values[max_range_idx]
                range_values[max_range_idx] = (low, high1)
                continue

            # if neither is included, need to check if the min is lower of another range and max is higher of another range
            # else, just add the new range
            extended_min, extend_min_idx = search_range_to_extend(low, high, range_values)
            while extended_min:
                del range_values[extend_min_idx]
                extended_min, extend_min_idx = search_range_to_extend(low, high, range_values)
                
            range_values.append((low, high))

            # TODO, for all cases there can be multiple ranges in the middle that need to be merged
            # This is not handled yet

        total = 0
        for r in range_values:
            print(f'Range: {r[0]}-{r[1]}')
            low, high = r
            total += (high - low + 1)

        print(total)
                

#part_1()
part_2()

        
