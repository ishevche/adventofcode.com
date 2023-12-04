def first(filename):
    with open(f"data/{filename}", 'r') as input_file:
        puzzle_input = [line.replace('\n', '') for line in input_file.readlines()]
    result = 0
    for line in puzzle_input:
        _, numbers = line.split(': ')
        winning, actual = numbers.split(' | ')
        winning = set(map(int, winning.split()))
        actual = set(map(int, actual.split()))
        power = sum([1 if my_number in winning else 0 for my_number in actual])
        if power == 0:
            continue
        result += 2 ** (power - 1)
    return result


def second(filename):
    with open(f"data/{filename}", 'r') as input_file:
        puzzle_input = [line.replace('\n', '') for line in input_file.readlines()]
    card_number = [1 for _ in puzzle_input]
    for idx, line in enumerate(puzzle_input):
        _, numbers = line.split(': ')
        winning, actual = numbers.split(' | ')
        winning = set(map(int, winning.split()))
        actual = set(map(int, actual.split()))
        power = sum([1 if my_number in winning else 0 for my_number in actual])
        for add in range(power):
            card_number[idx + add + 1] += card_number[idx]
    return sum(card_number)


if __name__ == '__main__':
    print(first("day4.txt"))
    print(second("day4.txt"))
