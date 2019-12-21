import math
from node import Node


def link_pathways(grid, z):
    # Link normal pathways
    for j in range(len(grid[z])):
        for i in range(len(grid[z][j])):
            node = grid[z][j][i]
            if node.value != ".":
                continue

            neighbor_indices = [(0, -1), (1, 0), (0, 1), (-1, 0)]
            for neighbor_index in neighbor_indices:
                neighbor = grid[z][j + neighbor_index[1]][i + neighbor_index[0]]
                if neighbor.value == ".":
                    node.neighbors.append(neighbor)


def find_portals(part_input):
    portals = {}
    # Go through the raw data and find portals and the nodes they attach to
    for j in range(len(part_input)):
        for i in range(len(part_input[j])):
            # Don't process the last column or row
            if i == len(part_input[j]) - 1 or j == len(part_input) - 1:
                continue

            portal_id = ""  # 2-long string, e.g. AA or ZZ
            connecting_point = None  # (x, y) of the connection points
            inner_node = True  # True if portal is in the inner side
            if i < 2 or j < 2 or i > len(part_input[j]) - 3 or j > len(part_input) - 3:
                inner_node = False

            if part_input[j][i].isalpha():
                portal_id += part_input[j][i]

                # Portals read down and right
                if part_input[j + 1][i].isalpha():
                    portal_id += part_input[j + 1][i]

                    if part_input[j - 1][i] == ".":
                        connecting_point = (i, j - 1)
                    else:
                        connecting_point = (i, j + 2)
                elif part_input[j][i + 1].isalpha():
                    portal_id += part_input[j][i + 1]

                    if part_input[j][i - 1] == ".":
                        connecting_point = (i - 1, j)
                    else:
                        connecting_point = (i + 2, j)

            if connecting_point is not None:
                if portal_id not in portals:
                    portals[portal_id] = []
                portals[portal_id].append((inner_node, connecting_point))

    return portals


def part1(part_input):
    print("PART1")

    # Link nodes, assign neighboring portal
    # Input grid has a padding of 2 on sides, so start from (2, 2)

    grid = [
        [
            [Node(i, j, 0, part_input[j][i]) for i in range(len(part_input[j]))]
            for j in range(len(part_input))
        ]
    ]

    link_pathways(grid, 0)

    # Parse portals
    portals = find_portals(part_input)

    start = end = None
    for k, v in portals.items():
        if len(v) == 2:
            start_portal = grid[0][v[0][1][1]][v[0][1][0]]
            end_portal = grid[0][v[1][1][1]][v[1][1][0]]
            start_portal.neighbors.append(end_portal)
            end_portal.neighbors.append(start_portal)
        elif k == "AA":
            start = grid[0][v[0][1][1]][v[0][1][0]]
        elif k == "ZZ":
            end = grid[0][v[0][1][1]][v[0][1][0]]

    # Pathfinding, BFS
    print(start.find_node_depth(end))


def part2(part_input):
    print("PART2")

    portals = find_portals(part_input)
    # Sort the portal data such that outer portal is first
    for k, v in portals.items():
        v.sort(key=lambda x: x[0])

    # Build first level
    grid = [
        [
            [Node(i, j, 0, part_input[j][i]) for i in range(len(part_input[j]))]
            for j in range(len(part_input))
        ]
    ]

    link_pathways(grid, 0)

    # Assign start and end for search
    start = end = None
    for k, v in portals.items():
        if k == "AA":
            start = grid[0][v[0][1][1]][v[0][1][0]]
        elif k == "ZZ":
            end = grid[0][v[0][1][1]][v[0][1][0]]

    # Attempt with increasing recursion count
    recursion_depth = 0
    while True:
        recursion_depth += 1

        grid.append(
            [
                [
                    Node(i, j, recursion_depth, part_input[j][i])
                    for i in range(len(part_input[j]))
                ]
                for j in range(len(part_input))
            ]
        )

        # Link portals from upper level's inner to next levels' outer
        for k, v in portals.items():
            if len(v) != 2:
                continue

            outer_x, outer_y = v[0][1]
            inner_x, inner_y = v[1][1]
            inner_node = grid[recursion_depth - 1][inner_y][inner_x]
            outer_node = grid[recursion_depth][outer_y][outer_x]
            inner_node.neighbors.append(outer_node)
            outer_node.neighbors.append(inner_node)

        link_pathways(grid, recursion_depth)

        search_result = start.find_node_depth(end)
        if search_result is not None:
            print(search_result)
            break


if __name__ == "__main__":
    with open("input", "r") as input_file:
        input_file_contents = input_file.readlines()
        input_file_contents = list(
            map(lambda x: x.replace("\n", ""), input_file_contents)
        )
        part1(input_file_contents)
        part2(input_file_contents)
