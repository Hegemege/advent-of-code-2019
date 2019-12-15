from intcode import Intcode
import math


class Node:
    def __init__(self, x, y, value, parent=None):
        self.position = (x, y)
        self.value = value
        self.parent = parent
        self.neighbors = [None for i in range(4)]
        self.known_neighbour_count = 0
        self.depth = math.inf

    def set_depth(self, depth):
        self.depth = depth
        for neighbor in self.neighbors:
            if neighbor.value == 0:
                continue
            if neighbor.depth <= self.depth + 1:
                continue
            neighbor.set_depth(self.depth + 1)

    def add_neighbor(self, direction, neighbor):
        self.neighbors[direction - 1] = neighbor

    def get_unexplored_directions(self):
        directions = []
        for i in range(4):
            if self.neighbors[i] is None:
                directions.append(i + 1)
        return directions

    def get_backtrack_movement(self):
        if self.parent is None:
            return None
        if self.parent.position[1] < self.position[1]:
            return 1
        if self.parent.position[1] > self.position[1]:
            return 2
        if self.parent.position[0] < self.position[0]:
            return 3
        if self.parent.position[0] > self.position[0]:
            return 4

    def __hash__(self):
        return hash(str(self.position))


def opposite_direction(direction):
    return direction + 1 if direction % 2 != 0 else direction - 1


DIR_OFFSETS = [(0, -1), (0, 1), (-1, 0), (1, 0)]


def apply_direction(position, direction):
    offset = DIR_OFFSETS[direction - 1]
    return (position[0] + offset[0], position[1] + offset[1])


def update_neighbors(nodes):
    for key, value in nodes.items():
        if value.known_neighbour_count == 4:
            continue
        for unexplored_dir in value.get_unexplored_directions():
            position = apply_direction(value.position, unexplored_dir)
            if position in nodes:
                value.add_neighbor(unexplored_dir, nodes[position])
                nodes[position].add_neighbor(opposite_direction(unexplored_dir), value)
                value.known_neighbour_count += 1
                nodes[position].known_neighbour_count += 1


def print_nodes(nodes, droid):
    print_width = 50
    print("-" * print_width)
    node_repr = ["#", ".", "o"]
    for j in range(-print_width // 2, print_width // 2):
        for i in range(-print_width // 2, print_width // 2):
            if i == droid.position[0] and j == droid.position[1]:
                print("D", end="", flush=True)
            elif (i, j) in nodes:
                print(node_repr[nodes[(i, j)].value], end="", flush=True)
            else:
                print(" ", end="", flush=True)
        print()
    print("-" * print_width)


def part1(part_input):
    print("PART1")

    memory = parse_input_file(part_input)
    input_buffer = []
    output_buffer = []
    computer = Intcode(memory, input_buffer, output_buffer)

    # Initialize the droid on an open spot
    nodes = {}
    nodes[(0, 0)] = Node(0, 0, 1)
    droid = nodes[(0, 0)]

    # Run the program until the robot has finished mapping the whole area
    while True:
        movement_command = None
        current_unexplored = droid.get_unexplored_directions()

        # If we find a non-explored neighbor, navigate there
        for test_dir in current_unexplored:
            movement_command = test_dir
            break

        # Check if we need to backtrack
        if len(current_unexplored) == 0 or movement_command is None:
            backtrack_command = droid.get_backtrack_movement()
            if backtrack_command is not None:
                movement_command = backtrack_command

        # If the movement command is still Node, every path has been checked
        if movement_command is None:
            break

        # Run the program
        computer.input_buffer.append(movement_command)
        computer.run_program()
        output = computer.output_buffer.pop(0)

        next_position = apply_direction(droid.position, movement_command)
        if next_position not in nodes:
            nodes[next_position] = Node(
                next_position[0], next_position[1], output, droid
            )

            # Update the grid's neighbour relations
            update_neighbors(nodes)

        if output != 0:
            droid = nodes[next_position]

    # Find the shortest path to the oxygen system
    # Starting from the droid's current position (at the starting position)
    # do a A* search updating the depth of all nodes
    droid.set_depth(0)
    for k, v in nodes.items():
        if v.value == 2:
            print(v.depth)
            break

    return nodes


def part2(nodes):
    print("PART2")

    # Part 1 already gets a complete map
    # Reset all depths and set the oxygen system's depth at 0
    # Then get the maximum depth of all nodes
    oxygen_node = None
    for k, v in nodes.items():
        v.depth = math.inf
        if v.value == 2:
            oxygen_node = v

    oxygen_node.set_depth(0)

    max_depth = 0
    for k, v in nodes.items():
        if v.value != 1:
            continue
        if v.depth > max_depth:
            max_depth = v.depth
    print(max_depth)


def print_grid(grid):
    grid_repr = ["#", ".", "O"]
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
        nodes = part1(input_file_contents)
        part2(nodes)
