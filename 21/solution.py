from intcode import Intcode
import math


def data_to_ascii(data):
    return "".join(map(chr, data))


def ascii_to_data(data):
    return list(map(ord, data))


def part1(part_input):
    print("PART1")

    memory = parse_input_file(part_input)
    input_buffer = []
    output_buffer = []
    computer = Intcode(memory, input_buffer, output_buffer)

    # Feed instructions
    instructions = [
        "OR A T",  # Check that A, B or C has a hole
        "AND B T",
        "AND C T",
        "NOT T J",  # If any of ABC is a hole, set JUMP
        "AND D J",  # but only if 4th spot is free
        #
        "WALK",
    ]

    for instruction in instructions:
        for data_input in ascii_to_data(instruction):
            computer.set_input(data_input)
        computer.set_input(ord("\n"))

    computer.run_program()

    if len(computer.output_buffer) > 100:
        print(data_to_ascii(computer.output_buffer))
    else:
        print(data_to_ascii(computer.output_buffer[:-1]))
        print(computer.output_buffer[-1])


def part2(part_input):
    print("PART2")

    memory = parse_input_file(part_input)
    input_buffer = []
    output_buffer = []
    computer = Intcode(memory, input_buffer, output_buffer)

    # Feed instructions
    instructions = [
        # Part 1
        "OR A T",  # Check that A, B or C has a hole
        "AND B T",
        "AND C T",
        "NOT T J",  # If any of ABC is a hole, set JUMP
        "AND D J",  # but only if 4th spot is free
        # Part 2
        # Jump only if we can jump immediately (H),
        # or after 1 step (E and I),
        # or if 2nd step is possible too (E and F)
        # ->
        # H or (E and I) or (E and F) ->
        # H or (E and (I or F))
        "OR I T",
        "OR F T",
        "AND E T",
        "OR H T",
        "AND T J",
        #
        "RUN",
    ]

    for instruction in instructions:
        for data_input in ascii_to_data(instruction):
            computer.set_input(data_input)
        computer.set_input(ord("\n"))

    computer.run_program()

    if len(computer.output_buffer) > 100:
        print(data_to_ascii(computer.output_buffer))
    else:
        print(data_to_ascii(computer.output_buffer[:-1]))
        print(computer.output_buffer[-1])


def parse_input_file(input_file_contents):
    return list(map(int, input_file_contents.split(",")))


if __name__ == "__main__":
    with open("input", "r") as input_file:
        input_file_contents = input_file.readline().strip()
        part1(input_file_contents)
        part2(input_file_contents)
