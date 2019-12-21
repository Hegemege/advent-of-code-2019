import math


class Node:
    def __init__(self, x, y, value):
        self.position = (x, y)
        self.value = value
        self.neighbors = []
        self.depth = math.inf
        self.neighbor_portal = None

    def find_node_depth(self, target):
        self.depth = 0
        visited = set()

        # Initialize BFS
        visited.add(self.position)
        boundary = [] + self.neighbors
        for neighbor in self.neighbors:
            neighbor.depth = self.depth + 1

        while len(boundary) > 0:
            extend = boundary.pop(0)
            if extend is target:
                return extend.depth

            if extend.position in visited:
                continue

            visited.add(extend.position)

            for neighbor in extend.neighbors:
                neighbor.depth = min(neighbor.depth, extend.depth + 1)

            boundary += extend.neighbors

