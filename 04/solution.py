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


def password_is_valid_part2(password):
    password = str(password)
    # Check duplicate adjacent and non-decreasing values
    adjacent = False
    adjacent_count = 1
    previous = None
    for symbol in password:
        if symbol == previous:
            adjacent_count += 1
        else:
            # Numbers change in the middle - condition satisfied if it was exactly 2 long
            if adjacent_count == 2:
                adjacent = True
            adjacent_count = 1
        if previous is not None and symbol < previous:
            return False
        previous = symbol
    # End of number can also contain one with 2 adjacent, so detect them here
    return adjacent or adjacent_count == 2


def part1(part_input):
    print(sum(map(password_is_valid, range(part_input[0], part_input[1] + 1))))


def part2(part_input):
    print(sum(map(password_is_valid_part2, range(
        part_input[0], part_input[1] + 1))))


if __name__ == '__main__':
    with open('input', 'r') as input_file:
        input_data = input_file.readline().strip()
        input_range = list(map(int, input_data.split('-')))
        part1(input_range)
        part2(input_range)
