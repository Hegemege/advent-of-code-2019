from intcode import Intcode
import math


def data_to_ascii(data):
    return "".join(map(chr, data))


def ascii_to_data(data):
    return list(map(ord, data))


def part1(part_input):
    print("PART1")

    computers = []
    initial_memory = parse_input_file(part_input)
    for i in range(50):
        input_buffer = []
        output_buffer = []
        computer = Intcode(initial_memory[:], input_buffer, output_buffer)
        computer.set_input(i)
        computers.append(computer)

        computer.run_program()

    network_messages = []
    while True:
        # Pass messages to machines
        for message in network_messages:
            # If address is 255, print and exit
            if message[0] == 255:
                print(message[2])
                return
            # Pass X and Y as input to the computer
            address, X, Y = message
            computers[address].set_input(X)
            computers[address].set_input(Y)

        network_messages.clear()

        # If there is no input, pass -1
        for computer in computers:
            if len(computer.input_buffer) == 0:
                computer.set_input(-1)

        for computer in computers:
            computer.run_program()

        # Get output
        for computer in computers:
            if len(computer.output_buffer) == 0:
                continue

            address = computer.output_buffer.pop(0)
            X = computer.output_buffer.pop(0)
            Y = computer.output_buffer.pop(0)
            network_messages.append((address, X, Y))


def part2(part_input):
    print("PART2")


def parse_input_file(input_file_contents):
    return list(map(int, input_file_contents.split(",")))


if __name__ == "__main__":
    with open("input", "r") as input_file:
        input_file_contents = input_file.readline().strip()
        part1(input_file_contents)
        part2(input_file_contents)
