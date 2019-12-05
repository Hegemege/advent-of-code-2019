MAX_INST_PARAM_COUNT = 3


def run_program(memory, input_buffer):
    pc = 0
    while True:
        result_code, pc_offset = execute_instruction(memory, pc, input_buffer)
        if result_code != 0:
            return
        pc += pc_offset


def execute_instruction(memory, position, input_buffer):
    instruction_header = memory[position]
    op_code = int(str(instruction_header)[-2:])
    if op_code == 99:
        return (1, 1)

    # Get parameter modes and pad the rest
    parameter_modes_str = str(instruction_header)[:-2][::-1]
    parameter_modes_str = parameter_modes_str.ljust(MAX_INST_PARAM_COUNT, '0')
    parameter_modes = list(map(int, parameter_modes_str))

    if op_code == 1 or op_code == 2:
        operator = int.__add__ if op_code == 1 else int.__mul__
        operand1_value = memory[position + 1]
        operand2_value = memory[position + 2]
        operand1 = memory[operand1_value] if parameter_modes[0] == 0 else operand1_value
        operand2 = memory[operand2_value] if parameter_modes[1] == 0 else operand2_value
        write_addr = memory[position + 3]

        memory[write_addr] = operator(operand1, operand2)

        return (0, 4)

    if op_code == 3:
        write_addr = memory[position + 1]
        input_value = input_buffer.pop(0)
        print("IN".ljust(6, ' ') + str(input_value))
        memory[write_addr] = input_value
        return (0, 2)

    if op_code == 4:
        operand_value = memory[position + 1]
        output_value = memory[operand_value] if parameter_modes[0] == 0 else operand_value
        print("OUT".ljust(6, ' ') + str(output_value))
        return (0, 2)


def part1(part_input):
    memory = parse_input_file(part_input)
    input_buffer = [1]
    run_program(memory, input_buffer)


def part2(part_input):
    pass


def parse_input_file(input_file_contents):
    return list(map(int, input_file_contents.split(",")))


if __name__ == '__main__':
    with open('input', 'r') as input_file:
        input_file_contents = input_file.readline()
        part1(input_file_contents)
        part2(input_file_contents)
