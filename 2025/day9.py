import os

def part_1():
    with open(os.path.join(os.path.dirname(__file__), 'tiles.txt'), 'r') as file:
        # read lines
        content = file.read()
        point_list = content.splitlines()
        points = [tuple(map(int, line.split(','))) for line in point_list]
        biggest_area = 0
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                area = abs(points[i][0] - points[j][0]+1) * abs(points[i][1] - points[j][1]+1)
                if area > biggest_area:
                    biggest_area = area

        print(biggest_area)

def point_inside_perimeter(point, points):
    y,x = point
    # use ray-casting algorithm to determine if point is inside polygon
    # points is a list of consecutive corners of the polygon
    # points on the perimeter are considered inside
    n = len(points)
    inside = False
    p1y, p1x = points[0]
    for i in range(n + 1):
        p2y, p2x = points[i % n]
        if y >= min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    print(f"Point {point} is [{'inside' if inside else 'outside'}] the perimeter")
    return inside

grid = []
def create_grid():
    global grid
    with open(os.path.join(os.path.dirname(__file__), 'tiles_test.txt'), 'r') as file:
        # read lines
        content = file.read()
        point_list = content.splitlines()
        points = [tuple(map(int, line.split(','))) for line in point_list]
        max_x = max(point[0] for point in points)
        max_y = max(point[1] for point in points)
        grid = [['.' for _ in range(max_x + 1)] for _ in range(max_y + 1)]
        for i in range(len(points)):
            x, y = points[i]
            grid[y][x] = '#'
            next_point = points[i+1] if i + 1 < len(points) else points[0]
            next_x, next_y = next_point
            # draw an x on each element between the two points
            if x == next_x:
                for j in range(min(y, next_y), max(y, next_y) + 1):
                    grid[j][x] = 'x'
            elif y == next_y:
                for j in range(min(x, next_x), max(x, next_x) + 1):
                    grid[y][j] = 'x'
        
def print_grid():
    global grid
    for row in grid:
        print(' '.join(row))

def part_2():
    global grid
    create_grid()
    with open(os.path.join(os.path.dirname(__file__), 'tiles_test.txt'), 'r') as file:
        # read lines
        content = file.read()
        point_list = content.splitlines()
        points = [tuple(map(int, line.split(','))) for line in point_list]
        biggest_area = 0
        for i in range(len(points)):
            for j in range(i+1, len(points)):
                area = abs(points[i][0] - points[j][0]+1) * abs(points[i][1] - points[j][1]+1)
                # we need to check if a third corner exists to form a rectangle
                #if area > biggest_area:
                create_grid()
                first_corner = points[i]
                second_corner = points[j]
                third_corner = (points[i][0], points[j][1])
                fourth_corner = (points[j][0], points[i][1])
                grid[first_corner[1]][first_corner[0]] = '1'
                grid[second_corner[1]][second_corner[0]] = '2'
                grid[third_corner[1]][third_corner[0]] = '3'
                grid[fourth_corner[1]][fourth_corner[0]] = '4'
                print(f"third_corner: {third_corner}, fourth_corner: {fourth_corner}")
                print_grid()
                #print(f"Rectangle of area {area} found with corners: {points[i]}, {points[j]}, {third_corner}, {fourth_corner}")
                # if third corner and fourth corner are inside the perimeter formed by points
                if area > biggest_area and point_inside_perimeter(third_corner, points) and point_inside_perimeter(fourth_corner, points):
                    biggest_area = area

        print(biggest_area)

part_2()

        
        

#print_grid()