class Node:
    def __init__(self, identifier):
        self.identifier = identifier
        self.parent = None
        self.children = []
        self.depth = 0

    def set_depth(self, depth):
        self.depth = depth
        for child in self.children:
            child.set_depth(depth + 1)


def part1(part_input):
    # Create nodes for every object in the data
    object_lookup = {}
    for orbit in part_input:
        objects = orbit.split(')')
        for symbol in objects:
            if symbol not in object_lookup:
                object_lookup[symbol] = Node(symbol)

    # Assign parent/child relationships
    for orbit in part_input:
        parent, child = tuple(
            map(lambda x: object_lookup[x], orbit.split(')'))
        )
        parent.children.append(child)
        child.parent = parent

    # Calculate depth of the tree. COM starts at 0 depth
    object_lookup["COM"].set_depth(0)

    # Sum the depths of every node
    print(sum(map(lambda x: x.depth, object_lookup.values())))


def part2(part_input):
    pass


if __name__ == '__main__':
    with open('input', 'r') as input_file:
        input_file_contents = list(map(str.strip, input_file.readlines()))
        part1(input_file_contents)
        part2(input_file_contents)
