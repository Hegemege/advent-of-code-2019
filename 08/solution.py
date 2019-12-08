import math

LAYER_SIZE = 25*6


def part1(part_input):
    layers = [part_input[i:i+LAYER_SIZE]
              for i in range(0, len(part_input), LAYER_SIZE)]

    find_layer = None
    zeros = math.inf
    for layer in layers:
        if layer.count('0') < zeros:
            zeros = layer.count('0')
            find_layer = layer

    print(find_layer.count('1') * find_layer.count('2'))


def part2(part_input):
    pass


if __name__ == '__main__':
    with open('input', 'r') as input_file:
        input_file_contents = input_file.readline().strip()
        part1(input_file_contents)
        part2(input_file_contents)
