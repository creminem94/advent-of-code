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


def part_2():
    with open(os.path.join(os.path.dirname(__file__), 'tiles.txt'), 'r') as file:
        # read lines
        content = file.read()
        point_list = content.splitlines()
        points = [tuple(map(int, line.split(','))) for line in point_list]
        biggest_area = 0
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                area = abs(points[i][0] - points[j][0]+1) * abs(points[i][1] - points[j][1]+1)
                # we need to check if a third corner exists to form a rectangle
                if area > biggest_area:
                    third_corner = (points[i][0], points[j][1])
                    fourth_corner = (points[j][0], points[i][1])
                    if third_corner in points or fourth_corner in points:
                        biggest_area = area

        print(biggest_area)

part_2()