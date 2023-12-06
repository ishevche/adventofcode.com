from math import sqrt, ceil, floor


def positive_integers_amount(a, b, c):
    discr = b * b - 4 * a * c
    lower = (b - sqrt(discr)) / 2
    upper = (b + sqrt(discr)) / 2
    lower_round = ceil(lower)
    upper_round = floor(upper)
    if lower_round == lower: lower_round += 1
    if upper_round == upper: upper_round -= 1
    return upper_round - lower_round + 1


def first(filename):
    with open(f"data/{filename}", 'r') as input_file:
        puzzle_input = [line.replace('\n', '') for line in input_file.readlines()]

    times = map(int, puzzle_input[0].split(':')[1].split())
    distances = map(int, puzzle_input[1].split(':')[1].split())
    result = 1
    for time, dist in zip(times, distances):
        result *= positive_integers_amount(-1, time, -dist)
    return result


def second(filename):
    with open(f"data/{filename}", 'r') as input_file:
        puzzle_input = [line.replace('\n', '') for line in input_file.readlines()]

    time = int(puzzle_input[0].split(':')[1].replace(' ', ''))
    dist = int(puzzle_input[1].split(':')[1].replace(' ', ''))
    return positive_integers_amount(-1, time, -dist)


if __name__ == '__main__':
    print(first("day6.txt"))
    print(second("day6.txt"))
