from enum import Enum


class ShuffleType(Enum):
    DEALINTONEWSTACK = 1
    CUT = 2
    DEALWITHINCREMENT = 3


def part1(part_input):
    print("PART1")

    DECK_SIZE = 10007
    deck = list(range(DECK_SIZE))
    instructions = []

    for row in part_input:
        if "cut" in row:
            instructions.append((ShuffleType.CUT, int(row.split(" ")[-1])))
        elif "new" in row:
            instructions.append((ShuffleType.DEALINTONEWSTACK,))
        elif "with" in row:
            instructions.append(
                (ShuffleType.DEALWITHINCREMENT, int(row.split(" ")[-1]))
            )

    for instruction in instructions:
        if instruction[0] == ShuffleType.DEALINTONEWSTACK:
            deck = deck[::-1]
        elif instruction[0] == ShuffleType.CUT:
            param = instruction[1]
            if abs(param) < DECK_SIZE:
                deck = deck[param:] + deck[:param]
        elif instruction[0] == ShuffleType.DEALWITHINCREMENT:
            param = instruction[1]
            new_deck = [None for i in range(DECK_SIZE)]
            for i in range(DECK_SIZE):
                index = (i * param) % DECK_SIZE
                new_deck[index] = deck[i]
            deck = new_deck

    print(deck.index(2019))


def part2(part_input):
    print("PART2")


if __name__ == "__main__":
    with open("input", "r") as input_file:
        input_file_contents = list(map(str.strip, input_file.readlines()))
        part1(input_file_contents)
        part2(input_file_contents)
