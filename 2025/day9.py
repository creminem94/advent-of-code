import os

point_cache = {}

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

def point_inside_perimeter(point, points, log=False):
    global point_cache
    if point in point_cache:
        return point_cache[point]
    x,y = point
    # use ray-casting algorithm to determine if point is inside polygon
    # points is a list of consecutive corners of the polygon
    # points on the perimeter are considered inside

    # for now, just go the right
    inside = False
    for i in range(len(points)):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % len(points)]
        if y1 > y2:
            x1, y1, x2, y2 = x2, y2, x1, y1  # ensure y1 <= y2
        if y == y1 or y == y2:  # point is on a horizontal edge
            if min(x1, x2) <= x <= max(x1, x2):
                if log:
                    print(f"Point {point} is on the perimeter")
                point_cache[point] = True
                return True
        # check if point is on vertical edge
        if x1 == x2 and min(y1, y2) <= y <= max(y1, y2):
            if x == x1:
                if log:
                    print(f"Point {point} is on the perimeter")
                point_cache[point] = True
                return True
        if (y > y1) != (y > y2):  # ray crosses the edge
            intersection_x = (x2 - x1) * (y - y1) / (y2 - y1) + x1
            if intersection_x >= x:  # ray intersects to the right of the point
                inside = not inside

    if log:
        print(f"Point {point} is [{'inside' if inside else 'outside'}] the perimeter")
    point_cache[point] = inside
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
    debug = False

    file_name = 'tiles_test.txt' if debug else 'tiles.txt'
    with open(os.path.join(os.path.dirname(__file__), file_name), 'r') as file:
        # read lines
        content = file.read()
        point_list = content.splitlines()
        points = [tuple(map(int, line.split(','))) for line in point_list]
        biggest_area = 0
        for i in range(len(points)):
            for j in range(i+1, len(points)):
                first_corner = points[i]
                second_corner = points[j]
                third_corner = (points[i][0], points[j][1])
                fourth_corner = (points[j][0], points[i][1])
                area = (abs(first_corner[0] - second_corner[0])+1) * (abs(first_corner[1] - second_corner[1])+1)
                # we need to check if a third corner exists to form a rectangle
                if debug:
                    create_grid()
                    grid[first_corner[1]][first_corner[0]] = '1'
                    grid[second_corner[1]][second_corner[0]] = '2'
                    grid[third_corner[1]][third_corner[0]] = '3'
                    grid[fourth_corner[1]][fourth_corner[0]] = '4'
                    print(f"\n1: {first_corner}, 2: {second_corner}")
                    print(f"3: {third_corner}, 4: {fourth_corner}")
                    print_grid()
                    print(f"Rectangle of area {area} found with corners: {points[i]}, {points[j]}, {third_corner}, {fourth_corner}")
                # if third corner and fourth corner are inside the perimeter formed by points
                
                    if check_validity((third_corner, fourth_corner), points, debug=debug) and area > biggest_area:
                        biggest_area = area
                elif area > biggest_area and check_validity((third_corner, fourth_corner), points, debug=debug):
                    biggest_area = area 

        print(biggest_area)

def check_validity(opposite_corners, perimeter_points, debug=False):
    return point_inside_perimeter(opposite_corners[0], perimeter_points) and point_inside_perimeter(opposite_corners[1], perimeter_points) and area_inside_perimeter(opposite_corners, perimeter_points)

def side_inside_perimeter(side_points, perimeter_points):
    # we have the two points of the side, check if all points between them are inside the perimeter
    (x1, y1), (x2, y2) = side_points
    if x1 == x2:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if not point_inside_perimeter((x1, y), perimeter_points):
                return False
    elif y1 == y2:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            if not point_inside_perimeter((x, y1), perimeter_points):
                return False
    return True

# area inside perimeter
def area_inside_perimeter(opposite_corners, perimeter_points):
    # it works but is not efficient
    (x1, y1), (x2, y2) = opposite_corners
    # check if all sides are inside perimeter
    side1 = ((x1, y1), (x1, y2))
    side2 = ((x1, y2), (x2, y2))
    side3 = ((x2, y2), (x2, y1))
    side4 = ((x2, y1), (x1, y1))
    area_inside = (side_inside_perimeter(side1, perimeter_points) and
            side_inside_perimeter(side2, perimeter_points) and
            side_inside_perimeter(side3, perimeter_points) and
            side_inside_perimeter(side4, perimeter_points))
    print(f"Area {'inside' if area_inside else 'not inside'} perimeter")
    return area_inside

part_2()
