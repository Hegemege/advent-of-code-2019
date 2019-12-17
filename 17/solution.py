from intcode import Intcode
import math


def part1(part_input):
    print("PART1")

    memory = parse_input_file(part_input)
    input_buffer = []
    output_buffer = []
    computer = Intcode(memory, input_buffer, output_buffer)

    computer.run_program()

    output_ascii = list(map(chr, computer.output_buffer))
    output_grid = "".join(output_ascii).split("\n")

    # Detect intersections
    calibration_sum = 0
    for j in range(1, len(output_grid) - 1):
        for i in range(1, len(output_grid[j]) - 1):
            if output_grid[j][i] != "#":
                continue

            if (
                output_grid[j][i - 1] == "#"
                and output_grid[j][i + 1] == "#"
                and output_grid[j - 1][i] == "#"
                and output_grid[j + 1][i] == "#"
            ):
                calibration_sum += i * j

    print(calibration_sum)


def part2(part_input):
    print("PART2")

    memory = parse_input_file(part_input)
    input_buffer = []
    output_buffer = []
    computer = Intcode(memory, input_buffer, output_buffer)

    # Active mode
    # computer.set_memory(0, 2)

    computer.run_program()

    output_ascii = list(map(chr, computer.output_buffer))
    output_grid = "".join(output_ascii).split("\n")

    for row in output_grid:
        print(row)


def parse_input_file(input_file_contents):
    return list(map(int, input_file_contents.split(",")))


if __name__ == "__main__":
    with open("input", "r") as input_file:
        input_file_contents = input_file.readline().strip()
        part1(input_file_contents)
        part2(input_file_contents)
