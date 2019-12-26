HEIGHT = 5
WIDTH = 5


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


class Grid:
    def __init__(self, recursive, initial=None):
        self.recursive = recursive
        self.nodes = [
            [
                Node(i, j, initial[j][i] if initial is not None else ".")
                for i in range(WIDTH)
            ]
            for j in range(HEIGHT)
        ]

        if recursive:
            self.nodes[HEIGHT // 2][WIDTH // 2] = None

        # Assign neighbours
        for j in range(HEIGHT):
            for i in range(WIDTH):
                node = self.nodes[j][i]
                if node is None:
                    continue

                # Right
                if i < WIDTH - 1:
                    other = self.nodes[j][i + 1]
                    if other is not None:
                        node.neighbors.append(other)
                        other.neighbors.append(node)

                # Down
                if j < HEIGHT - 1:
                    other = self.nodes[j + 1][i]
                    if other is not None:
                        node.neighbors.append(other)
                        other.neighbors.append(node)

    def get_rating(self):
        return sum(
            [
                self.nodes[j][i].value * (2 ** (i + WIDTH * j))
                for j in range(HEIGHT)
                for i in range(WIDTH)
            ]
        )

    def update_next_value(self):
        for j in range(HEIGHT):
            for i in range(WIDTH):
                node = self.nodes[j][i]
                if node is None:
                    continue
                node.update_next_value()

    def assign_next_value(self):
        for j in range(HEIGHT):
            for i in range(WIDTH):
                node = self.nodes[j][i]
                if node is None:
                    continue
                node.assign_next_value()

    def check_expand_out(self):
        for j in range(HEIGHT):
            for i in range(WIDTH):
                node = self.nodes[j][i]
                if node is None:
                    continue
                if i == 0 or j == 0 or i == WIDTH - 1 or j == HEIGHT - 1:
                    if node.value == 1:
                        return True
        return False

    def check_expand_in(self):
        center_x = WIDTH // 2
        center_y = HEIGHT // 2

        if (
            self.nodes[center_y - 1][center_x].value == 1
            or self.nodes[center_y][center_x + 1].value == 1
            or self.nodes[center_y + 1][center_x].value == 1
            or self.nodes[center_y][center_x - 1].value == 1
        ):
            return True

        return False

    def link_outer(self, other):
        """
            Links the edge of self to the inner nodes of the given Grid
        """
        center_x = WIDTH // 2
        center_y = HEIGHT // 2

        other_top = other.nodes[center_y - 1][center_x]
        other_right = other.nodes[center_y][center_x + 1]
        other_bottom = other.nodes[center_y + 1][center_x]
        other_left = other.nodes[center_y][center_x - 1]

        for i in range(WIDTH):
            # Top row
            self.nodes[0][i].neighbors.append(other_top)
            other_top.neighbors.append(self.nodes[0][i])
            # Bottom row
            self.nodes[HEIGHT - 1][i].neighbors.append(other_bottom)
            other_bottom.neighbors.append(self.nodes[HEIGHT - 1][i])

        for j in range(HEIGHT):
            # Left column
            self.nodes[j][0].neighbors.append(other_left)
            other_left.neighbors.append(self.nodes[j][0])
            # Right column
            self.nodes[j][WIDTH - 1].neighbors.append(other_right)
            other_right.neighbors.append(self.nodes[j][WIDTH - 1])

    def get_bug_count(self):
        return sum(
            map(
                lambda x: sum(map(lambda y: y.value if y is not None else 0, x)),
                self.nodes,
            )
        )


def part1(part_input):
    print("PART1")

    grid = Grid(False, part_input)

    seen_states = set()

    while True:
        state_id = grid.get_rating()

        if state_id in seen_states:
            print(state_id)
            return

        seen_states.add(state_id)

        grid.update_next_value()
        grid.assign_next_value()


def part2(part_input):
    print("PART2")

    grids = [Grid(True, part_input)]
    top_layer = grids[0]
    bottom_layer = grids[0]

    for i in range(200):
        # Check if top or bottom layer needs to expand
        # for the next iteration
        if top_layer.check_expand_out():
            new_top_layer = Grid(True)
            top_layer.link_outer(new_top_layer)
            top_layer = new_top_layer
            grids.append(new_top_layer)

        if bottom_layer.check_expand_in():
            new_bottom_layer = Grid(True)
            new_bottom_layer.link_outer(bottom_layer)
            bottom_layer = new_bottom_layer
            grids.append(new_bottom_layer)

        for grid in grids:
            grid.update_next_value()
        for grid in grids:
            grid.assign_next_value()

    print(sum(map(lambda x: x.get_bug_count(), grids)))


if __name__ == "__main__":
    with open("input", "r") as input_file:
        input_file_contents = list(map(str.strip, input_file.readlines()))
        part1(input_file_contents)
        part2(input_file_contents)
