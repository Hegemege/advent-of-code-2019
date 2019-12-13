from intcode import Intcode


def part1(part_input):
    print("PART1")

    memory = parse_input_file(part_input)
    input_buffer = []
    output_buffer = []

    computer = Intcode(memory, input_buffer, output_buffer)

    grid = [[0 for i in range(100)] for j in range(100)]

    computer.run_program()
    while True:
        if len(computer.output_buffer) == 0:
            break

        x = computer.output_buffer.pop(0)
        y = computer.output_buffer.pop(0)
        tile_id = computer.output_buffer.pop(0)

        grid[y][x] = tile_id

    print(sum(map(lambda x: x.count(2), grid)))


def part2(part_input):
    print("PART2")

    memory = parse_input_file(part_input)
    input_buffer = []
    output_buffer = []

    computer = Intcode(memory, input_buffer, output_buffer)

    grid = [[0 for i in range(50)] for j in range(50)]

    score = 0

    computer.run_program()
    while True:
        if len(computer.output_buffer) == 0:
            break

        x = computer.output_buffer.pop(0)
        y = computer.output_buffer.pop(0)
        tile_id = computer.output_buffer.pop(0)

        if x == -1 and y == 0:
            score = tile_id
        else:
            grid[y][x] = tile_id

    grid_repr = [".", "#", "B", "-", "x"]
    for j in range(len(grid)):
        for i in range(len(grid[0])):
            cell = grid[j][i]
            print(grid_repr[cell], end="", flush=True)
        print()


def parse_input_file(input_file_contents):
    return list(map(int, input_file_contents.split(",")))


if __name__ == "__main__":
    with open("input", "r") as input_file:
        input_file_contents = input_file.readline().strip()
        part1(input_file_contents)
        part2(input_file_contents)
