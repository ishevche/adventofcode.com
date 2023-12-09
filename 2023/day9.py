def predict_next(sequence):
    if all(map(lambda x: x == 0, sequence)):
        return 0
    diff = [sequence[idx] - sequence[idx - 1] for idx in range(1, len(sequence))]
    return sequence[-1] + predict_next(diff)


def first(filename):
    with open(f"data/{filename}", 'r') as input_file:
        puzzle_input = [line.replace('\n', '') for line in input_file.readlines()]
    puzzle_input = list(map(lambda x: list(map(int, x.split())), puzzle_input))
    return sum(map(predict_next, puzzle_input))


def predict_past(sequence):
    if all(map(lambda x: x == 0, sequence)):
        return 0
    diff = [sequence[idx] - sequence[idx - 1] for idx in range(1, len(sequence))]
    return sequence[0] - predict_past(diff)


def second(filename):
    with open(f"data/{filename}", 'r') as input_file:
        puzzle_input = [line.replace('\n', '') for line in input_file.readlines()]
    puzzle_input = list(map(lambda x: list(map(int, x.split())), puzzle_input))
    return sum(map(predict_past, puzzle_input))


if __name__ == '__main__':
    print(first("day9.txt"))
    print(second("day9.txt"))
