import math
from functools import reduce


class Moon:
    def __init__(self, pos, axis_count=3):
        self.axis_count = axis_count
        self.pos = [pos[i] for i in range(self.axis_count)]
        self.vel = [0 for i in range(self.axis_count)]

    def apply_gravity(self, other):
        # Applies gravity for both objects
        for i in range(self.axis_count):
            if self.pos[i] < other.pos[i]:
                self.vel[i] += 1
                other.vel[i] -= 1
            elif self.pos[i] > other.pos[i]:
                self.vel[i] -= 1
                other.vel[i] += 1

    def update_position(self):
        for i in range(self.axis_count):
            self.pos[i] += self.vel[i]

    def get_energy(self):
        return sum(map(abs, self.pos)) * sum(map(abs, self.vel))

    def __str__(self):
        return str(tuple(self.pos) + tuple(self.vel))


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

    # Simulate each axis once
    # The time it takes for the whole system to reset can
    # be calculated by computing the least common multiple of
    # the individual cycles

    cycles = []

    for i in range(3):
        coords = parse_input(part_input)
        coords = [[x[i]] for x in coords]  # Map only to the wanted axis
        moons = [Moon(pos, 1) for pos in coords]

        visited = set()

        # Set starting position as visited
        start_hash = hash(",".join(map(str, moons)))
        visited.add(start_hash)

        while True:
            # Apply gravity
            for moon_index in range(len(moons)):
                for other_moon_index in range(moon_index, len(moons)):
                    moons[moon_index].apply_gravity(moons[other_moon_index])

            # Update position
            for moon in moons:
                moon.update_position()

            # Check if we have visited this state before
            moon_hash = hash(",".join(map(str, moons)))
            if moon_hash in visited:
                break

            visited.add(moon_hash)

        cycles.append(len(visited))

    # Find the least common multiple of the cycles
    lcm = cycles[0]
    for i in cycles[1:]:
        lcm = lcm * i // math.gcd(lcm, i)

    print(lcm)


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
