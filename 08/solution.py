import math

LAYER_WIDTH = 25
LAYER_HEIGHT = 6
LAYER_SIZE = LAYER_WIDTH*LAYER_HEIGHT


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
    layers = [part_input[i:i+LAYER_SIZE]
              for i in range(0, len(part_input), LAYER_SIZE)]

    image_data = [2 for i in range(LAYER_SIZE)]

    for layer in layers:
        for i in range(LAYER_SIZE):
            layer_pixel = layer[i]
            image_pixel = image_data[i]

            if image_pixel == 2:
                image_data[i] = int(layer_pixel)

    pixel_repr = ['.', '#', ' ']

    for j in range(LAYER_HEIGHT):
        row_str = ''
        for i in range(LAYER_WIDTH):
            row_str += pixel_repr[int(image_data[i + j * LAYER_WIDTH])]
        print(row_str)


if __name__ == '__main__':
    with open('input', 'r') as input_file:
        input_file_contents = input_file.readline().strip()
        part1(input_file_contents)
        part2(input_file_contents)
