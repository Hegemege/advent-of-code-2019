import math
from node import Node


def part1(part_input):
    print("PART1")

    # Link nodes, assign neighboring portal
    # Input grid has a padding of 2 on sides, so start from (2, 2)

    grid = [
        [Node(i, j, part_input[j][i]) for i in range(len(part_input[j]))]
        for j in range(len(part_input))
    ]

    # Link normal pathways
    for j in range(len(grid)):
        for i in range(len(grid[j])):
            node = grid[j][i]
            if node.value != ".":
                continue

            neighbor_indices = [(0, -1), (1, 0), (0, 1), (-1, 0)]
            for neighbor_index in neighbor_indices:
                neighbor = grid[j + neighbor_index[1]][i + neighbor_index[0]]
                if neighbor.value == ".":
                    node.neighbors.append(neighbor)

    # Parse portals
    portals = {}
    # Go through the raw data and find portals and the nodes they attach to
    for j in range(len(part_input)):
        for i in range(len(part_input[j])):
            # Don't process the last column or row
            if i == len(part_input[j]) - 1 or j == len(part_input) - 1:
                continue
            portal_id = ""
            connecting_node = None
            if part_input[j][i].isalpha():
                portal_id += part_input[j][i]
                # Portals read down and right
                if part_input[j + 1][i].isalpha():
                    portal_id += part_input[j + 1][i]
                    if part_input[j - 1][i] == ".":
                        connecting_node = grid[j - 1][i]
                    else:
                        connecting_node = grid[j + 2][i]
                elif part_input[j][i + 1].isalpha():
                    portal_id += part_input[j][i + 1]
                    if part_input[j][i - 1] == ".":
                        connecting_node = grid[j][i - 1]
                    else:
                        connecting_node = grid[j][i + 2]
            if connecting_node is not None:
                if portal_id not in portals:
                    portals[portal_id] = []
                portals[portal_id].append(connecting_node)

    start = end = None
    for k, v in portals.items():
        if len(v) == 2:
            v[0].neighbors.append(v[1])
            v[1].neighbors.append(v[0])
        elif k == "AA":
            start = v[0]
        elif k == "ZZ":
            end = v[0]

    # Pathfinding, BFS
    print(start.find_node_depth(end))


def part2(part_input):
    print("PART2")


if __name__ == "__main__":
    with open("input", "r") as input_file:
        input_file_contents = input_file.readlines()
        input_file_contents = list(
            map(lambda x: x.replace("\n", ""), input_file_contents)
        )
        part1(input_file_contents)
        part2(input_file_contents)
