import itertools
import math


MAX_INST_PARAM_COUNT = 3
PRINT_IO = False


class Intcode:
    def __init__(self, memory, input_buffer, output_buffer):
        self.memory = memory
        self.input_buffer = input_buffer
        self.output_buffer = output_buffer
        self.pc = 0
        self.relative_base = 0
        self.input_count = 0
        self.memory_size = len(self.memory)

    def run_program(self):
        if self.pc is None:
            return None

        while True:
            result_code, pc_offset, wait = self.execute_instruction()
            if result_code == -1:  # Halt instruction
                return None
            if result_code == 0:  # Non-jump instructions
                self.pc += pc_offset
            elif result_code == 1:  # Jump instructions
                self.pc = pc_offset

            if wait:  # Waiting for input
                return self.pc

    def execute_instruction(self):
        instruction_header = self.get_memory(self.pc)
        op_code = int(str(instruction_header)[-2:])

        # Halt instruction
        if op_code == 99:
            return (-1, 1, False)

        # Get parameter modes and pad the rest
        parameter_modes_str = str(instruction_header)[:-2][::-1]
        parameter_modes_str = parameter_modes_str.ljust(MAX_INST_PARAM_COUNT, "0")
        parameter_modes = list(map(int, parameter_modes_str))

        # Add and multiply
        if op_code == 1 or op_code == 2:
            operator = int.__add__ if op_code == 1 else int.__mul__
            parameter1 = self.get_parameter(1, parameter_modes)
            parameter2 = self.get_parameter(2, parameter_modes)
            write_addr = self.get_write_addr(3, parameter_modes)
            write_value = operator(parameter1, parameter2)

            self.set_memory(write_addr, write_value)

            return (0, 4, False)

        # Input
        elif op_code == 3:
            # If we need to wait for input, return (0, 0) so pc won't advance
            if self.input_count == 0:
                return (0, 0, True)
            input_value = self.input_buffer.pop(0)
            self.input_count -= 1
            write_addr = self.get_write_addr(1, parameter_modes)
            if PRINT_IO:
                print("IN".ljust(6, " ") + str(input_value))
            self.set_memory(write_addr, input_value)
            return (0, 2, False)

        # Output
        elif op_code == 4:
            output_value = self.get_parameter(1, parameter_modes)
            if PRINT_IO:
                print("OUT".ljust(6, " ") + str(output_value))
            self.output_buffer.append(output_value)
            return (0, 2, False)

        # Jump-if-true && jump-if-false
        elif op_code == 5 or op_code == 6:
            parameter1 = self.get_parameter(1, parameter_modes)
            parameter2 = self.get_parameter(2, parameter_modes)

            # A XNOR B, it just works
            if (parameter1 == 0) == (op_code == 5):
                return (0, 3, False)

            # Parameter 2 holds the PC value to jump to
            return (1, parameter2, False)

        # Less-than && equals
        elif op_code == 7 or op_code == 8:
            operator = int.__lt__ if op_code == 7 else int.__eq__
            parameter1 = self.get_parameter(1, parameter_modes)
            parameter2 = self.get_parameter(2, parameter_modes)
            write_addr = self.get_write_addr(3, parameter_modes)
            write_value = 1 if operator(parameter1, parameter2) else 0

            self.set_memory(write_addr, write_value)

            return (0, 4, False)

        elif op_code == 9:
            parameter1 = self.get_parameter(1, parameter_modes)
            self.relative_base += parameter1
            return (0, 2, False)

        print("OPCODE NOT IMPLEMENTED:", op_code)

    def get_parameter(self, offset, parameter_modes):
        parameter_mode = parameter_modes[offset - 1]
        parameter_value = self.get_memory(self.pc + offset)
        if parameter_mode == 0:
            return self.get_memory(parameter_value)
        elif parameter_mode == 1:
            return parameter_value
        elif parameter_mode == 2:
            addr = self.relative_base + parameter_value
            return self.get_memory(addr)

        print("PARAMETER MODE NOT IMPLEMENTED:", parameter_mode)

    def get_write_addr(self, offset, parameter_modes):
        parameter_mode = parameter_modes[offset - 1]
        parameter_value = self.get_memory(self.pc + offset)
        if parameter_mode == 0:
            return parameter_value
        elif parameter_mode == 2:
            addr = self.relative_base + parameter_value
            return addr

        print("PARAMETER MODE NOT IMPLEMENTED:", parameter_mode)

    def get_memory(self, position):
        # if position < 0:
        #     print("ACCESSING NEGATIVE MEMORY POSITION")
        #     quit()
        if position >= self.memory_size:
            # Memory not accessed before is all 0's
            return 0
        return self.memory[position]

    def set_memory(self, position, value):
        if position >= self.memory_size:
            # Expand memory
            expansion = position - self.memory_size + 1
            self.memory = self.memory + expansion * [0]
            self.memory_size += expansion

        self.memory[position] = value

    def set_input(self, value):
        self.input_buffer.append(value)
        self.input_count += 1
