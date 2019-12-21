import math
from state import SearchState
from node import Node


def part1(part_input):
    print("PART1")

    # Create a search space of collecting the keys in a specified order
    # Actions between states are navigations from current position to
    # the next key through the shortest path

    grid = [
        [Node(i, j, part_input[j][i]) for i in range(len(part_input[0]))]
        for j in range(len(part_input))
    ]

    # Assign neighbors to grid cells
    # No need to assign to the outer edge, since it's all solid walls anyways
    for j in range(1, len(grid) - 1):
        for i in range(1, len(grid[0]) - 1):
            node = grid[j][i]
            if grid[j - 1][i].value != "#":
                node.neighbors.append(grid[j - 1][i])
            if grid[j + 1][i].value != "#":
                node.neighbors.append(grid[j + 1][i])
            if grid[j][i - 1].value != "#":
                node.neighbors.append(grid[j][i - 1])
            if grid[j][i + 1].value != "#":
                node.neighbors.append(grid[j][i + 1])

    key_position_lookup = {}

    # Starting state
    state = SearchState()

    # Add keys to lookup
    key_position_lookup["@"] = (0, 0)  # First key for making iterations easier
    for j in range(len(grid)):
        for i in range(len(grid[j])):
            node = grid[j][i]
            if (
                node.value != "#"  # No walls
                and node.value != "."  # No empty space
                and (
                    node.value == "@"  # Starting point behaves like a key
                    or node.value == node.lowervalue  # Actual keys
                )
            ):
                key_position_lookup[node.value] = (i, j)

    # Create a lookup for shortest paths between keys
    # Key is (from, to) as symbols, value is a list of tuples
    # [(path_length, required_keys)]
    key_shortest_path_lookup = {}
    keys = list(key_position_lookup.keys())
    for key_index in range(len(keys)):
        key = keys[key_index]
        for other_key_index in range(key_index + 1, len(keys)):
            other_key = keys[other_key_index]
            # Add empty arrays to cache
            key_shortest_path_lookup[(key, other_key)] = []
            key_shortest_path_lookup[(other_key, key)] = []
            # # Clear the grid
            # for row in grid:
            #     for node in row:
            #         node.depth = math.inf
            #         node.parent = None
            # x, y = key_position_lookup[key]
            # tx, ty = key_position_lookup[other_key]
            # grid[y][x].set_depth_probe(0)
    #
    # path_length = grid[ty][tx].depth
    # path_doors = grid[ty][tx].find_parent_doors([])
    # key_shortest_path_lookup[(key, other_key)] = (path_length, path_doors)

    # Set the starting key as always picked
    state.keys_picked.add("@")
    state.position = key_position_lookup["@"]
    state.current_key = "@"
    for key in keys:
        if key == "@":
            continue
        state.keys_missing.add(key)

    search_stack = [state]
    shortest_solution_length = math.inf

    while len(search_stack) > 0:
        current_state = search_stack.pop()

        if (
            current_state.step_count < shortest_solution_length
            and current_state.is_terminal_state()
        ):
            shortest_solution_length = current_state.step_count
            print(
                "New shortest",
                shortest_solution_length,
                "stack size",
                len(search_stack),
            )

        for action in current_state.get_actions(
            grid, key_position_lookup, key_shortest_path_lookup
        ):
            clone = current_state.clone()
            clone.apply_action(action)

            # Only deepend the search if we haven't found a way better solution already
            if clone.step_count < shortest_solution_length:
                search_stack.append(clone)

    print(shortest_solution_length)


def part2(part_input):
    print("PART2")


if __name__ == "__main__":
    with open("input", "r") as input_file:
        input_file_contents = input_file.readlines()
        input_file_contents = list(map(str.strip, input_file_contents))
        part1(input_file_contents)
        part2(input_file_contents)
