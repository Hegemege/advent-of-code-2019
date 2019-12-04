def password_is_valid(password):
    password = str(password)
    # Check duplicate adjacent and non-decreasing values
    adjacent = False
    previous = None
    for symbol in password:
        if symbol == previous:
            adjacent = True
        if previous is not None and symbol < previous:
            return False
        previous = symbol

    return adjacent


def part1(part_input):
    print(sum(map(password_is_valid, range(part_input[0], part_input[1] + 1))))


def part2(part_input):
    pass


if __name__ == '__main__':
    with open('input', 'r') as input_file:
        input_data = input_file.readline().strip()
        input_range = list(map(int, input_data.split('-')))
        part1(input_range)
        part2(input_range)
