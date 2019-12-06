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

    def get_ancestors(self, ancestors):
        if self.parent is None:
            return ancestors

        ancestors.append(self.parent)
        return self.parent.get_ancestors(ancestors)


def build_tree(part_input):
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

    return object_lookup


def part1(part_input):
    object_lookup = build_tree(part_input)
    # Sum the depths of every node
    print(sum(map(lambda x: x.depth, object_lookup.values())))


def part2(part_input):
    object_lookup = build_tree(part_input)
    # Find the first common ancestor of YOU and SAN
    # i.e. the common ancestor with largest depth
    # Sum the steps required to reach that ancestor
    you_orbit = object_lookup["YOU"].parent
    san_orbit = object_lookup["SAN"].parent

    you_ancestors = you_orbit.get_ancestors([])
    san_ancestors = san_orbit.get_ancestors([])

    common_ancestors = set(you_ancestors).intersection(set(san_ancestors))

    first_common_ancestor = max(common_ancestors, key=lambda x: x.depth)
    # Solution is the distance between the common ancestor and the target nodes summed
    print(you_orbit.depth - first_common_ancestor.depth +
          san_orbit.depth - first_common_ancestor.depth)


if __name__ == '__main__':
    with open('input', 'r') as input_file:
        input_file_contents = list(map(str.strip, input_file.readlines()))
        part1(input_file_contents)
        part2(input_file_contents)
