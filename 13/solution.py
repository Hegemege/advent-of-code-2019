from intcode import Intcode
import math

WIDTH = 46
HEIGHT = 30


def part1(part_input):
    print("PART1")

    memory = parse_input_file(part_input)
    input_buffer = []
    output_buffer = []

    computer = Intcode(memory, input_buffer, output_buffer)

    grid = [[0 for i in range(WIDTH)] for j in range(HEIGHT)]

    computer.run_program()
    parse_output(computer, grid)

    print(sum(map(lambda x: x.count(2), grid)))


def part2(part_input):
    print("PART2")

    memory = parse_input_file(part_input)
    input_buffer = []
    output_buffer = []

    # Set the coin counter
    memory[0] = 2

    computer = Intcode(memory, input_buffer, output_buffer)

    grid = [[0 for i in range(WIDTH)] for j in range(HEIGHT)]

    # Run one step to get the paddle and ball positions
    computer.run_program()
    parse_output(computer, grid)

    paddle = [0, 0]
    ball = [0, 0]

    score = 0
    while True:
        if sum(map(lambda x: x.count(2), grid)) == 0:
            break

        # Update ball and paddle positions
        for j in range(len(grid)):
            for i in range(len(grid[j])):
                if grid[j][i] == 4:
                    ball = [i, j]
                elif grid[j][i] == 3:
                    paddle = [i, j]

        # Check which direction to move the paddle
        if ball[0] == paddle[0]:
            computer.input_buffer.append(0)
        elif ball[0] < paddle[0]:
            computer.input_buffer.append(-1)
        else:
            computer.input_buffer.append(1)

        # Run the program
        computer.run_program()
        score = parse_output(computer, grid)

        # Print the grid
        # print_grid(grid)

    print(score)


def print_grid(grid):
    grid_repr = [".", "#", "B", "-", "x"]
    for j in range(len(grid)):
        for i in range(len(grid[0])):
            cell = grid[j][i]
            print(grid_repr[cell], end="", flush=True)
        print()


def parse_output(computer, grid):
    score = 0

    while True:
        if len(computer.output_buffer) == 0:
            break

        x = computer.output_buffer.pop(0)
        y = computer.output_buffer.pop(0)
        tile_id = computer.output_buffer.pop(0)

        if x == -1 and y == 0:
            score = tile_id
        else:
            grid[y][x] = tile_id

    return score


def parse_input_file(input_file_contents):
    return list(map(int, input_file_contents.split(",")))


if __name__ == "__main__":
    with open("input", "r") as input_file:
        input_file_contents = input_file.readline().strip()
        part1(input_file_contents)
        part2(input_file_contents)
