import math


def get_score(grid, x, y, width, height):
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
    # Naive approach
    # Assume square grid
    height = len(part_input)
    width = len(part_input[0])

    best_score = 0
    for j in range(height):
        for i in range(width):
            if part_input[j][i] != '#':
                continue

            grid = [[part_input[j][i]
                     for i in range(width)] for j in range(height)]
            score = get_score(grid, i, j, width, height)
            if score > best_score:
                print("Highest", score, i, j)
                best_score = score

    print(best_score)


def part2(part_input):
    print("PART2")


if __name__ == '__main__':
    with open('input', 'r') as input_file:
        input_file_contents = list(map(str.strip, input_file.readlines()))
        part1(input_file_contents)
        part2(input_file_contents)
