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

    while True:
        computer.run_program()
        print(data_to_ascii(computer.output_buffer))

        command = input()
        if command == "exit":
            return

        data = ascii_to_data(command)
        for code in data:
            computer.set_input(code)
        computer.set_input(ord("\n"))


def part2(part_input):
    print("PART2")


def parse_input_file(input_file_contents):
    return list(map(int, input_file_contents.split(",")))


if __name__ == "__main__":
    with open("input", "r") as input_file:
        input_file_contents = input_file.readline().strip()
        part1(input_file_contents)
        part2(input_file_contents)
