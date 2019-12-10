import math


def detect_asteroids(grid, x, y, width, height):
    # Loop in circles centered on x, y
    # If an asteroid is found, repeat the same vector behind the asteroid
    # and set all of those spots empty
    # Finally return the sum of all asteroids

    visible_count = 0

    radius = 0
    while radius < len(grid):
        radius += 1

        for j in range(y - radius, y + radius + 1):
            for i in range(x - radius, x + radius + 1):
                if i < 0 or j < 0 or i >= width or j >= height:
                    continue

                if grid[j][i] != '#':
                    continue

                visible_count += 1
                # Vector from x,y to i,j is (i - x, j - y)
                direction = (i - x, j - y)

                # i,j == x,y
                if direction[0] == 0 and direction[1] == 0:
                    continue

                # Reduce the direction vector to shortest possible
                # using math.gcd()
                gcd = math.gcd(abs(direction[0]), abs(direction[1]))
                if (gcd > 0):
                    direction = ((i - x) // gcd, (j - y) // gcd)

                # Repeat vector until out of range and set each position empty
                iteration = 1
                while True:
                    iteration += 1
                    offset = tuple([iteration * n for n in direction])

                    hide_x = x + offset[0]
                    hide_y = y + offset[1]

                    # Do not hide the found asteroid, though
                    if hide_x == i and hide_y == j:
                        continue

                    if hide_x < 0 or hide_y < 0 or hide_x >= width or hide_y >= height:
                        break
                    grid[hide_y][hide_x] = '.'

    # Subtract 1 (the asteroid itself)
    return sum(map(lambda x: x.count('#'), grid)) - 1


def part1(part_input):
    print("PART1")
    # Naive approach
    # Assume square grid
    height = len(part_input)
    width = len(part_input[0])

    best_score = 0
    best_grid = None
    best_position = None
    for j in range(height):
        for i in range(width):
            if part_input[j][i] != '#':
                continue

            grid = [[part_input[j][i]
                     for i in range(width)] for j in range(height)]
            score = detect_asteroids(grid, i, j, width, height)
            if score > best_score:
                print("Highest", score, i, j)
                best_score = score
                best_grid = grid
                best_position = (i, j)

    print(best_score)

    return best_grid, best_position


def part2(grid, position):
    print("PART2")
    # Reuse part1's grid
    # Less than 1 rotation is required because 309 are detected (200 required)
    # This simplifies, because we don't have to run the detector many times and remove
    # any asteroids

    # Run the detector once - only visible asteroids remain
    # Collect them in a list and sort by angle

    height = len(grid)
    width = len(grid[0])

    grid[position[1]][position[0]] = 'x'

    # Get a list of asteroid locations
    # Also change the coordinate system to be centered on the position
    asteroid_locations = [(i - position[0], j - position[1]) for i in range(
        width) for j in range(height) if grid[j][i] == '#']

    # atan2 is angle between X axis and the vector from origin to x,y
    # We need to go clockwise instead of counter-clockwise, so use -y
    # We also need to then add 0.5*pi because we want to start up, not right
    angles = [math.atan2(-asteroid[1], asteroid[0]) * -1 + math.pi * 0.5
              for asteroid in asteroid_locations]

    # Angles in the last quadrant are still going to be negative
    # Add +2 pi to any negative value
    angles = [angle if angle >= 0 else angle + math.pi*2 for angle in angles]

    # Sort and keep index
    sorted_angles = [i for i in sorted(enumerate(angles), key=lambda x:x[1])]
    twohundreth = asteroid_locations[sorted_angles[199][0]]
    # Return to grid coordinate system
    print((twohundreth[0] + position[0])*100 + twohundreth[1] + position[1])


if __name__ == '__main__':
    with open('input', 'r') as input_file:
        input_file_contents = list(map(str.strip, input_file.readlines()))
        grid, pos = part1(input_file_contents)
        part2(grid, pos)
