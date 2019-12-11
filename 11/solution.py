from intcode import Intcode


def part1(part_input):
    print("PART1")

    memory = parse_input_file(part_input)
    input_buffer = []
    output_buffer = []

    computer = Intcode(memory, input_buffer, output_buffer)

    grid = [[0 for i in range(200)] for j in range(200)]

    robot_pos = (len(grid)//2, len(grid)//2)
    robot_dir = 0
    dir_lookup = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    visited = set()

    while True:
        step_x, step_y = robot_pos
        step_input = grid[step_y][step_x]
        input_buffer.append(step_input) 

        exit_code = computer.run_program()
        if exit_code is None:
            break

        next_color = output_buffer.pop(0)
        next_dir = output_buffer.pop(0)

        visited.add(robot_pos)
        grid[step_y][step_x] = next_color
        next_dir = next_dir * 2 - 1
        robot_dir = (robot_dir + next_dir) % 4
        move_offset = dir_lookup[robot_dir]
        robot_pos = (robot_pos[0] + move_offset[0], robot_pos[1] + move_offset[1])


    print(len(visited))


def part2(part_input):
    print("PART2")

    memory = parse_input_file(part_input)
    input_buffer = []
    output_buffer = []

    computer = Intcode(memory, input_buffer, output_buffer)

    grid = [[0 for i in range(100)] for j in range(100)]

    robot_pos = (len(grid)//2, len(grid)//2)

    grid[robot_pos[1]][robot_pos[0]] = 1

    robot_dir = 0
    dir_lookup = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    visited = set()

    while True:
        step_x, step_y = robot_pos
        step_input = grid[step_y][step_x]
        input_buffer.append(step_input) 

        exit_code = computer.run_program()
        if exit_code is None:
            break

        next_color = output_buffer.pop(0)
        next_dir = output_buffer.pop(0)

        visited.add(robot_pos)
        grid[step_y][step_x] = next_color
        next_dir = next_dir * 2 - 1
        robot_dir = (robot_dir + next_dir) % 4
        move_offset = dir_lookup[robot_dir]
        robot_pos = (robot_pos[0] + move_offset[0], robot_pos[1] + move_offset[1])


    print(len(visited))

    for row in grid:
        row_str = ['.' if item == 0 else '#' for item in row]
        print(''.join(row_str))

def parse_input_file(input_file_contents):
    return list(map(int, input_file_contents.split(",")))


if __name__ == '__main__':
    with open('input', 'r') as input_file:
        input_file_contents = input_file.readline().strip()
        part1(input_file_contents)
        part2(input_file_contents)
