class Node:
    def __init__(self, x, y, value):
        self.position = (x, y)
        self.value = 0 if value == "." else 1
        self.next_value = None
        self.neighbors = []

    def update_next_value(self):
        neighbor_sum = sum(map(lambda x: x.value, self.neighbors))
        self.next_value = 0
        if self.value == 0 and (neighbor_sum == 1 or neighbor_sum == 2):
            self.next_value = 1
        elif self.value == 1 and neighbor_sum == 1:
            self.next_value = 1

    def assign_next_value(self):
        self.value = self.next_value


def part1(part_input):
    print("PART1")

    nodes = [
        [Node(i, j, part_input[j][i]) for i in range(len(part_input[j]))]
        for j in range(len(part_input))
    ]

    # Assign neighbours
    for j in range(len(nodes)):
        for i in range(len(nodes[j])):
            node = nodes[j][i]
            # Right
            if i < len(nodes[j]) - 1:
                node.neighbors.append(nodes[j][i + 1])
                nodes[j][i + 1].neighbors.append(node)
            # Down
            if j < len(nodes) - 1:
                node.neighbors.append(nodes[j + 1][i])
                nodes[j + 1][i].neighbors.append(node)

    seen_states = set()

    while True:
        state_id = sum(
            [
                nodes[j][i].value * (2 ** (i + len(nodes[j]) * j))
                for j in range(len(nodes))
                for i in range(len(nodes[j]))
            ]
        )

        if state_id in seen_states:
            print(state_id)
            return

        seen_states.add(state_id)

        for row in nodes:
            for node in row:
                node.update_next_value()

        for row in nodes:
            for node in row:
                node.assign_next_value()


def part2(part_input):
    print("PART2")


if __name__ == "__main__":
    with open("input", "r") as input_file:
        input_file_contents = list(map(str.strip, input_file.readlines()))
        part1(input_file_contents)
        part2(input_file_contents)
