AXIS_COUNT = 3


class Moon:
    def __init__(self, pos):
        self.pos = [pos[i] for i in range(AXIS_COUNT)]
        self.vel = [0 for i in range(AXIS_COUNT)]

    def apply_gravity(self, other):
        # Applies gravity for both objects
        for i in range(AXIS_COUNT):
            if self.pos[i] < other.pos[i]:
                self.vel[i] += 1
                other.vel[i] -= 1
            elif self.pos[i] > other.pos[i]:
                self.vel[i] -= 1
                other.vel[i] += 1

    def update_position(self):
        for i in range(AXIS_COUNT):
            self.pos[i] += self.vel[i]

    def get_energy(self):
        return sum(map(abs, self.pos)) * sum(map(abs, self.vel))


def part1(part_input):
    print("PART1")

    coords = parse_input(part_input)
    moons = [Moon(pos) for pos in coords]

    for i in range(1000):
        # Apply gravity
        for moon_index in range(len(moons)):
            for other_moon_index in range(moon_index, len(moons)):
                moons[moon_index].apply_gravity(moons[other_moon_index])

        # Update position
        for moon in moons:
            moon.update_position()

    print(sum(map(lambda x: x.get_energy(), moons)))


def part2(part_input):
    print("PART2")


def parse_input(part_input):
    return [
        [
            int(axis)
            for axis in pos.replace("<", "")
            .replace(">", "")
            .replace("=", "")
            .replace(" ", "")
            .replace("x", "")
            .replace("y", "")
            .replace("z", "")
            .strip()
            .split(",")
        ]
        for pos in part_input
    ]


if __name__ == "__main__":
    with open("input", "r") as input_file:
        input_file_contents = input_file.readlines()
        part1(input_file_contents)
        part2(input_file_contents)
