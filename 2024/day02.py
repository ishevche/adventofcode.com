def check_safe(levels):
    for i in range(1, len(levels)):
        levels[i - 1] = levels[i] - levels[i - 1]
    max_diff = max(levels[:-1])
    min_diff = min(levels[:-1])
    if (max_diff <= 3 and min_diff >= 1) or \
            (max_diff <= -1 and min_diff >= -3):
        return True


def first(puzzle_input):
    safe = 0
    for line in puzzle_input:
        levels = list(map(int, line.split()))
        if check_safe(levels):
            safe += 1
    return safe


def second(puzzle_input):
    safe = 0
    for line in puzzle_input:
        levels = list(map(int, line.split()))
        for i in range(0, len(levels)):
            if check_safe(levels[:i] + levels[i + 1:]):
                safe += 1
                break
    return safe


def solve(filename, solve_func):
    with open(f"data/{filename}", 'r') as input_file:
        puzzle_input = [line.replace('\n', '') for line in input_file.readlines()]
    return solve_func(puzzle_input)


if __name__ == '__main__':
    print(solve("day02.txt", first))
    print(solve("day02.txt", second))
