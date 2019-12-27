import math


def create_pattern_lookup(length):
    """
        Create a lookup list for the multiplication pattern
        [0, 1, 0, -1] where each index is repeated N times
        and the first value is removed

        pattern_lookup[0] = [1, 0, -1, 0, 1, 0, -1, ...]
        pattern_lookup[1] = [0, 1, 1, 0, 0, -1, -1, 0, 0, 1, 1, ...]
        pattern_lookup[2] = [0, 0, 1, 1, 1, 0, 0, 0, -1, -1, -1, 0, 0, 0, 1, 1, 1, ...]
    """
    pattern_lookup = []
    # Create pattern lookups for all indices
    for i in range(length):
        pattern_lookup.append([])

        pattern_value = 0
        pattern_dir = 1
        pattern_wait = i

        for j in range(length + 1):
            pattern_lookup[i].append(pattern_value)

            if pattern_wait == 0:
                pattern_wait = i
                pattern_value += pattern_dir
                # Swap the direction to achieve 0, 1, 0, -1; 0, 1, 0, ...
                if abs(pattern_value) != 0:
                    pattern_dir *= -1
            else:
                pattern_wait -= 1

        # Remove the first element
        pattern_lookup[i].pop(0)

    return pattern_lookup


def part1(part_input):
    print("PART1")

    pattern_lookup = create_pattern_lookup(len(part_input))

    input_signal = part_input
    for _ in range(100):
        output_signal = [0 for i in input_signal]

        # Convert the signal
        for i in range(len(input_signal)):
            pattern = pattern_lookup[i]
            output_signal[i] = (
                abs(
                    sum(
                        [pattern[j] * input_signal[j] for j in range(len(input_signal))]
                    )
                )
                % 10
            )

        input_signal = output_signal

    print("".join(map(str, input_signal[:8])))


def part2(part_input):
    print("PART2")

    signal = part_input * 10000

    # offset it past the midpoint, no need to check any values below it
    # Only additions of digits, fft multipliers are 0's and 1's
    offset = int("".join([str(n) for n in signal[:7]]))

    for _ in range(100):
        n_sum = sum(signal[offset:])
        for n in range(offset, len(signal)):
            # Current multipliers are   000...01111...1
            # Next multipliers are      000...00111...1
            # Add the numbers together and for the next row, subtract current
            old = signal[n]
            signal[n] = n_sum % 10
            n_sum -= old

    print("".join(map(str, part_input[offset : offset + 8])))


def parse_input_line(line):
    return [int(x) for x in line]


if __name__ == "__main__":
    with open("input", "r") as input_file:
        input_file_contents = input_file.readline().strip()
        # Convert to an array of numbers
        part1(parse_input_line(input_file_contents))
        part2(parse_input_line(input_file_contents))
