from intcode import Intcode


def part1(part_input):
    memory = parse_input_file(part_input)
    input_buffer = [1]
    output_buffer = []
    computer = Intcode(memory, input_buffer, output_buffer)
    computer.run_program()


def part2(part_input):
    pass


def parse_input_file(input_file_contents):
    return list(map(int, input_file_contents.split(",")))


if __name__ == '__main__':
    with open('input', 'r') as input_file:
        input_file_contents = input_file.readline().strip()
        part1(input_file_contents)
        part2(input_file_contents)
