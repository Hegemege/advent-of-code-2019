import math


class Node:
    def __init__(self, x, y, value):
        self.position = (x, y)
        self.value = value
        self.lowervalue = value.lower()
        self.uppervalue = value.upper()
        self.isKey = value == value.lower() and value != "." and value != "@"
        self.isDoor = value == value.upper() and value != "." and value != "@"
        self.neighbors = []
        self.depth = math.inf
        self.parent = None

    def set_depth(self, depth, keys_missing):
        self.depth = depth
        for neighbor in self.neighbors:
            # Early exits to stop recursing
            # If the neighbor is impassable
            if neighbor.value == "#":
                continue
            # If we already have a better path to that node
            if neighbor.depth <= self.depth + 1:
                continue
            # If there is no key
            if neighbor.isDoor and neighbor.lowervalue in keys_missing:
                continue
            neighbor.parent = self
            neighbor.set_depth(self.depth + 1, keys_missing)

    def set_depth_probe(self, depth):
        self.depth = depth
        for neighbor in self.neighbors:
            # Early exits to stop recursing
            # If the neighbor is impassable
            if neighbor.value == "#":
                continue
            # If we already have a better path to that node
            if neighbor.depth <= self.depth + 1:
                continue

            neighbor.parent = self
            neighbor.set_depth_probe(self.depth + 1)

    def find_parent_doors(self, doors):
        if self.parent is None:
            return doors

        if self.isDoor:
            doors.append(self.lowervalue)

        return self.parent.find_parent_doors(doors)
