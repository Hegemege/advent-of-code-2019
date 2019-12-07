import itertools
import math

MAX_INST_PARAM_COUNT = 3
PRINT_IO = False


def run_program(pc, memory, input_buffer, output_buffer):
    if pc is None:
        return None

    while True:
        result_code, pc_offset = execute_instruction(
            memory, pc, input_buffer, output_buffer)
        if result_code == -1:  # Halt instruction
            return None
        if result_code == 0:  # Non-jump instructions
            pc += pc_offset
        elif result_code == 1:  # Jump instructions
            pc = pc_offset

        if pc_offset == 0:  # Waiting for input
            return pc


def execute_instruction(memory, position, input_buffer, output_buffer):
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
        # If we need to wait for input, return (0, 0) so pc won't advance
        if len(input_buffer) == 0:
            return (0, 0)
        write_addr = memory[position + 1]
        input_value = input_buffer.pop(0)
        if PRINT_IO:
            print("IN".ljust(6, ' ') + str(input_value))
        memory[write_addr] = input_value
        return (0, 2)

    # Output
    if op_code == 4:
        output_value = get_parameter(memory, position, 1, parameter_modes)
        if PRINT_IO:
            print("OUT".ljust(6, ' ') + str(output_value))
        output_buffer.append(output_value)
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
    amp_permutations = list(
        itertools.permutations(range(AMP_COUNT), AMP_COUNT))
    highest_output = -math.inf
    for setting in amp_permutations:
        amp_input = 0
        for amp_index in range(AMP_COUNT):
            memory = parse_input_file(part_input)
            input_buffer = [setting[amp_index], amp_input]
            output_buffer = []
            run_program(0, memory, input_buffer, output_buffer)
            amp_input = output_buffer.pop()
        if amp_input > highest_output:
            highest_output = amp_input
    print(highest_output)


def part2(part_input):
    amp_permutations = list(itertools.permutations(
        range(5, 5 + AMP_COUNT), AMP_COUNT))
    highest_output = -math.inf

    for setting in amp_permutations:
        amp_memory = []
        input_buffers = list(map(lambda x: [x], setting))
        output_buffers = [[] for i in range(AMP_COUNT)]
        program_counters = [0 for i in range(AMP_COUNT)]

        # Initialize memory
        for amp_index in range(AMP_COUNT):
            amp_memory.append(parse_input_file(part_input))

        # Give initial 0 input to the first amp
        input_buffers[0].append(0)

        # Start running the programs. Store PC when the program ends until
        # None is returned from the final amp
        while True:
            for amp_index in range(AMP_COUNT):
                pc = program_counters[amp_index]
                memory = amp_memory[amp_index]
                input_buffer = input_buffers[amp_index]
                output_buffer = output_buffers[amp_index]

                new_pc = run_program(pc, memory, input_buffer, output_buffer)

                # Pass potential output to the next amplifier
                if len(output_buffer) > 0:
                    amp_output = output_buffer.pop()
                    next_amp_index = (amp_index + 1) % AMP_COUNT
                    input_buffers[next_amp_index].append(amp_output)

                # Store program counter
                program_counters[amp_index] = new_pc

            # The last amp will write it's output to the input of the first amp
            # anyways, so let's check it from there
            if input_buffers[0][0] > highest_output:
                highest_output = input_buffers[0][0]

            # Check if the programs have halted by checking the last amp
            if program_counters[-1] is None:
                break

    print(highest_output)


def parse_input_file(input_file_contents):
    return list(map(int, input_file_contents.split(",")))


AMP_COUNT = 5

if __name__ == '__main__':
    with open('input', 'r') as input_file:
        input_file_contents = input_file.readline()
        part1(input_file_contents)
        part2(input_file_contents)
