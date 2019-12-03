import operator
import math


def parse_step(step):
    '''
        Returns a 3-tuple (x_offset, y_offset, distance) for the given instruction
        E.g. step="D12" returns (0, -1, 12)
    '''
    symbol = step[0]
    distance = int(step[1:])
    if symbol == 'U':
        return (0, 1, distance)
    elif symbol == 'R':
        return (1, 0, distance)
    elif symbol == 'D':
        return (0, -1, distance)
    elif symbol == 'L':
        return (-1, 0, distance)


def part1(part_input):
    line1_steps = part_input[0].split(",")
    line2_steps = part_input[1].split(",")

    line1_visited = set()
    closest_intersection_distance = math.inf

    position = (0, 0)
    for step in line1_steps:
        parsed = parse_step(step)
        position_offset = parsed[:2]
        for i in range(parsed[2]):
            position = tuple(map(operator.add, position, position_offset))
            line1_visited.add(position)

    position = (0, 0)
    for step in line2_steps:
        parsed = parse_step(step)
        position_offset = parsed[:2]  # Slicing works for tuples!
        for i in range(parsed[2]):
            position = tuple(map(operator.add, position, position_offset))
            if position in line1_visited:
                distance = sum(map(abs, position))
                if distance < closest_intersection_distance:
                    closest_intersection_distance = distance

    print(closest_intersection_distance)


def part2(part_input):
    pass


if __name__ == '__main__':
    with open('input', 'r') as input_file:
        input_data = []
        input_data.append(input_file.readline().strip())
        input_data.append(input_file.readline().strip())

        part1(input_data)
        # part2()
