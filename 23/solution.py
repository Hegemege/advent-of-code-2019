from intcode import Intcode
import math


def data_to_ascii(data):
    return "".join(map(chr, data))


def ascii_to_data(data):
    return list(map(ord, data))


def main(part_input):
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
    nat_memory = None
    nat_sent_history = set()
    part1_complete = False
    while True:
        # Pass messages to machines
        for message in network_messages:
            # If address is 255, print and exit
            if message[0] == 255 and not part1_complete:
                part1_complete = True
                print(message[2])
                print("PART2")

            # Direct 255 to NAT
            if message[0] == 255:
                nat_memory = (0, message[1], message[2])
                continue

            # Pass X and Y as input to the computer
            address, X, Y = message
            computers[address].set_input(X)
            computers[address].set_input(Y)

        network_messages.clear()

        # If there is no input, pass -1
        # Monitor NAT
        network_active = False
        for computer in computers:
            if len(computer.input_buffer) == 0:
                computer.set_input(-1)
            elif part1_complete:
                network_active = True

        if part1_complete and not network_active:
            # Send NAT packet
            if nat_memory in nat_sent_history:
                print(nat_memory[2])
                break
            nat_sent_history.add(nat_memory)

            address = nat_memory[0]
            computers[address].set_input(nat_memory[1])
            computers[address].set_input(nat_memory[2])

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


def parse_input_file(input_file_contents):
    return list(map(int, input_file_contents.split(",")))


if __name__ == "__main__":
    with open("input", "r") as input_file:
        input_file_contents = input_file.readline().strip()
        main(input_file_contents)
