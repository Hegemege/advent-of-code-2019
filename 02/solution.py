def run_program(memory):
    pc = 0
    while True:
        if execute_instruction(memory, pc) != 0:
            return
        pc += 4


def execute_instruction(memory, position):
    if memory[position] == 99:
        return 1
    operator = int.__add__ if memory[position] == 1 else int.__mul__
    operand1 = memory[memory[position + 1]]
    operand2 = memory[memory[position + 2]]
    write_addr = memory[position + 3]

    memory[write_addr] = operator(operand1, operand2)

    return 0


def part1(part_input):
    memory = parse_input_file(part_input)

    # Modifications as per spec
    memory[1] = 12
    memory[2] = 2

    run_program(memory)

    print(memory[0])


def part2(part_input):
    for noun in range(0, 100):
        for verb in range(0, 100):
            memory = parse_input_file(part_input)

            memory[1] = noun
            memory[2] = verb

            run_program(memory)

            if memory[0] == 19690720:
                print(100 * noun + verb)
                return


def parse_input_file(input_file_contents):
    return list(map(int, input_file_contents.split(",")))


if __name__ == '__main__':
    with open('input', 'r') as input_file:
        input_file_contents = input_file.readline()
        part1(input_file_contents)
        part2(input_file_contents)
