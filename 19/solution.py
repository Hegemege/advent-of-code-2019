from intcode import Intcode
import math


def part1(part_input):
    print("PART1")

    GRID_SIZE = 50

    grid = [[0 for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]

    initial_memory = parse_input_file(part_input)
    input_buffer = []
    output_buffer = []

    last_point = (0, 0)

    for j in range(len(grid)):
        for i in range(len(grid[0])):
            memory = initial_memory[:]

            computer = Intcode(memory, input_buffer, output_buffer)

            computer.set_input(i)
            computer.set_input(j)

            computer.run_program()

            grid[j][i] = computer.output_buffer.pop()

            if grid[j][i] == 1:
                last_point = (i, j)

    print(sum([sum(row) for row in grid]))

    return last_point


def position_in_beam(initial_memory, input_buffer, output_buffer, position):
    memory = initial_memory[:]
    computer = Intcode(memory, input_buffer, output_buffer)
    computer.set_input(position[0])
    computer.set_input(position[1])

    computer.run_program()

    return computer.output_buffer.pop() == 1


def part2(part_input, last_point):
    print("PART2")

    SHIP_SIZE = 100

    # Pick the last point of the tractor beam found in Part 1
    # Zig-zag within the beam by traveling down and right alternately
    # until reaching the end of the beam, then switching

    # After distance between two turning points reaches SHIP_SIZE = 100, start
    # checking the diagonal width of the beam at those points, storing the previous
    # When the diagonal distance hits 100 or higher, travel backwards and
    # find the first such diagonal. The min(x1, x2) and min(y1, y2) are the
    # x and y coordinates of the topleft corner of the ship where
    # (x1, y1) and (x2, y2) are the ending points of the first
    # 100-long diagonal

    initial_memory = parse_input_file(part_input)
    input_buffer = []
    output_buffer = []

    current_position = last_point
    direction = 0  # 0 = down, 1 = right

    last_edge = current_position

    # Phase 1
    print("Phase 1, robot at", current_position)

    while True:
        query_position = (
            current_position[0] + direction,
            current_position[1] + 1 - direction,
        )

        query_in_beam = position_in_beam(
            initial_memory, input_buffer, output_buffer, query_position
        )

        if not query_in_beam:
            direction = 1 - direction
            # If distance to last edge is over SHIP_SIZE, move to phase 2 of the search
            if (
                current_position[0] - last_edge[0] + current_position[1] - last_edge[1]
                > SHIP_SIZE
            ):
                break
            last_edge = current_position
        else:
            current_position = query_position

    # Phase 2
    print("Phase 2, robot at", current_position)
    # current_position is now at one edge
    # At every edge after this, start tracking the width of the beam at 45 degrees
    while True:
        query_position = (
            current_position[0] + direction,
            current_position[1] + 1 - direction,
        )

        query_in_beam = position_in_beam(
            initial_memory, input_buffer, output_buffer, query_position
        )

        if not query_in_beam:
            direction = 1 - direction
            # Calculate width of the beam
            current_diagonal_position = current_position
            diagonal_direction_vector = (1, -1) if direction == 1 else (-1, 1)
            diagonal_width = 1
            while True:
                diagonal_query_position = (
                    current_diagonal_position[0] + diagonal_direction_vector[0],
                    current_diagonal_position[1] + diagonal_direction_vector[1],
                )

                diagonal_query_in_beam = position_in_beam(
                    initial_memory, input_buffer, output_buffer, diagonal_query_position
                )

                if diagonal_query_in_beam:
                    current_diagonal_position = diagonal_query_position
                    diagonal_width += 1
                else:
                    break

            # Check the diagonal width, move to Phase 3 if we found a wide
            # enough spot on the beam
            if diagonal_width >= SHIP_SIZE:
                break

            last_edge = current_position
        else:
            current_position = query_position

    # Phase 3
    # The first diagonal to fit the ship lies somewhere between
    # last_edge and current_position
    print("Phase 3, robot at", current_position, "last edge at", last_edge)

    # Travel forward from last_edge and check diagonal on every step
    direction = 1 - direction
    distance = current_position[0] - last_edge[0] + current_position[1] - last_edge[1]
    current_position = last_edge

    for i in range(distance):
        diagonal_width = 1

        # Check diagonal on one side of current position first
        current_diagonal_position = current_position
        diagonal_direction_vector = (1, -1) if direction == 1 else (-1, 1)

        diagonal_endpoints = [current_diagonal_position, current_diagonal_position]

        while True:
            diagonal_query_position = (
                current_diagonal_position[0] + diagonal_direction_vector[0],
                current_diagonal_position[1] + diagonal_direction_vector[1],
            )

            diagonal_query_in_beam = position_in_beam(
                initial_memory, input_buffer, output_buffer, diagonal_query_position
            )

            if diagonal_query_in_beam:
                current_diagonal_position = diagonal_query_position
                diagonal_width += 1
            else:
                diagonal_endpoints[0] = current_diagonal_position
                break

        # Return back to the middle and check the other side of current position
        current_diagonal_position = current_position
        diagonal_direction_vector = (
            -diagonal_direction_vector[0],
            -diagonal_direction_vector[1],
        )

        while True:
            diagonal_query_position = (
                current_diagonal_position[0] + diagonal_direction_vector[0],
                current_diagonal_position[1] + diagonal_direction_vector[1],
            )

            diagonal_query_in_beam = position_in_beam(
                initial_memory, input_buffer, output_buffer, diagonal_query_position
            )

            if diagonal_query_in_beam:
                current_diagonal_position = diagonal_query_position
                diagonal_width += 1
            else:
                diagonal_endpoints[1] = current_diagonal_position
                break

        print("Diagonal width", diagonal_width)
        if diagonal_width == SHIP_SIZE:
            # If we found the first diagonal with exact width, get the
            # min() of the end locations x's and y's respectively - the
            # ship's topleft corner is located there
            min_x = min(diagonal_endpoints[0][0], diagonal_endpoints[1][0])
            min_y = min(diagonal_endpoints[0][1], diagonal_endpoints[1][1])
            print("Top left at", min_x, min_y)
            print(min_x * 10000 + min_y)
            break
        else:
            # Otherwise advance to the next position
            current_position = (
                current_position[0] + direction,
                current_position[1] + 1 - direction,
            )


def parse_input_file(input_file_contents):
    return list(map(int, input_file_contents.split(",")))


if __name__ == "__main__":
    with open("input", "r") as input_file:
        input_file_contents = input_file.readline().strip()
        last_point = part1(input_file_contents)
        part2(input_file_contents, last_point)
