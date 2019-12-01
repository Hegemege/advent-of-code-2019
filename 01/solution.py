def f(x):
    return max(int(x / 3) - 2, 0)


def g(x, acc=0):
    fuel = f(x)
    if fuel == 0:
        return acc
    else:
        return g(fuel, acc + fuel)


def part1():
    with open('input', 'r') as file:
        print(sum(map(f, map(int, map(str.strip, file)))))


def part2():
    with open('input', 'r') as file:
        print(sum(map(g, map(int, map(str.strip, file)))))


if __name__ == '__main__':
    part1()
    part2()
