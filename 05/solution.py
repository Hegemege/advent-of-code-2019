MAX_INST_PARAM_COUNT = 3


def run_program(memory, input_buffer):
    pc = 0
    while True:
        result_code, pc_offset = execute_instruction(memory, pc, input_buffer)
        if result_code == -1:  # Halt instruction
            return
        if result_code == 0:  # Non-jump instructions
            pc += pc_offset
        elif result_code == 1:  # Jump instructions
            pc = pc_offset


def execute_instruction(memory, position, input_buffer):
    instruction_header = memory[position]
    op_code = int(str(instruction_header)[-2:])
    if op_code == 99:
        return (-1, 1)

    # Get parameter modes and pad the rest
    parameter_modes_str = str(instruction_header)[:-2][::-1]
    parameter_modes_str = parameter_modes_str.ljust(MAX_INST_PARAM_COUNT, '0')
    parameter_modes = list(map(int, parameter_modes_str))

    # Add and multiply
    if op_code == 1 or op_code == 2:
        operator = int.__add__ if op_code == 1 else int.__mul__
        parameter1 = get_parameter(memory, position, 1, parameter_modes)
        parameter2 = get_parameter(memory, position, 2, parameter_modes)
        write_addr = memory[position + 3]

        memory[write_addr] = operator(parameter1, parameter2)

        return (0, 4)

    # Input
    if op_code == 3:
        write_addr = memory[position + 1]
        input_value = input_buffer.pop(0)
        print("IN".ljust(6, ' ') + str(input_value))
        memory[write_addr] = input_value
        return (0, 2)

    # Output
    if op_code == 4:
        output_value = get_parameter(memory, position, 1, parameter_modes)
        print("OUT".ljust(6, ' ') + str(output_value))
        return (0, 2)

    # Jump-if-true && jump-if-false
    if op_code == 5 or op_code == 6:
        parameter1 = get_parameter(memory, position, 1, parameter_modes)
        parameter2 = get_parameter(memory, position, 2, parameter_modes)

        # A XNOR B
        if (parameter1 == 0) == (op_code == 5):
            return (0, 3)
        return (1, parameter2)

    # Less-than && equals
    if op_code == 7 or op_code == 8:
        operator = int.__lt__ if op_code == 7 else int.__eq__
        parameter1 = get_parameter(memory, position, 1, parameter_modes)
        parameter2 = get_parameter(memory, position, 2, parameter_modes)
        write_addr = memory[position + 3]

        memory[write_addr] = 1 if operator(parameter1, parameter2) else 0

        return (0, 4)

    print("OPCODE NOT IMPLEMENTED:", op_code)


def get_parameter(memory, position, offset, parameter_modes):
    return memory[memory[position + offset]] if parameter_modes[offset - 1] == 0 else memory[position + offset]


def part1(part_input):
    print("PART 1")
    memory = parse_input_file(part_input)
    input_buffer = [1]
    run_program(memory, input_buffer)


def part2(part_input):
    print("PART 2")
    memory = parse_input_file(part_input)
    input_buffer = [5]
    run_program(memory, input_buffer)


def parse_input_file(input_file_contents):
    return list(map(int, input_file_contents.split(",")))


if __name__ == '__main__':
    with open('input', 'r') as input_file:
        input_file_contents = input_file.readline()
        part1(input_file_contents)
        part2(input_file_contents)
