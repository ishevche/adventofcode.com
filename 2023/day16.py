directions = {
    '\\': {
        'U': ('L',),
        'R': ('D',),
        'D': ('R',),
        'L': ('U',),
    },
    '/': {
        'U': ('R',),
        'R': ('U',),
        'D': ('L',),
        'L': ('D',),
    },
    '-': {
        'U': ('R', 'L'),
        'R': ('R',),
        'D': ('R', 'L'),
        'L': ('L',),
    },
    '|': {
        'U': ('U',),
        'R': ('U', 'D'),
        'D': ('D',),
        'L': ('U', 'D'),
    },
    '.': {
        'U': ('U',),
        'R': ('R',),
        'D': ('D',),
        'L': ('L',),
    },
}

direction_number = {
    'U': 0,
    'R': 1,
    'D': 2,
    'L': 3
}


def count_energized(layout, starting_pos, direction):
    energized = [[False for _ in range(len(layout[0]))] for _ in range(len(layout))]
    stack = [(starting_pos, direction)]
    dirs = [[[False for _ in range(4)] for _ in range(len(energized[0]))] for _ in range(len(energized))]
    while stack:
        (x, y), cur_dir = stack.pop()
        if cur_dir == 'U':
            x -= 1
        if cur_dir == 'R':
            y += 1
        if cur_dir == 'D':
            x += 1
        if cur_dir == 'L':
            y -= 1
        if 0 <= x < len(energized) and 0 <= y < len(energized[x]):
            energized[x][y] = True
        else:
            continue
        for new_dir in directions[layout[x][y]][cur_dir]:
            if not dirs[x][y][direction_number[new_dir]]:
                stack.append(((x, y), new_dir))
                dirs[x][y][direction_number[new_dir]] = True
    return sum(map(lambda row: sum(map(int, row)), energized))


def first(puzzle_input):
    return count_energized(puzzle_input, (0, -1), 'R')


def second(puzzle_input):
    result = 0
    for row in range(len(puzzle_input)):
        result = max(result, count_energized(puzzle_input, (row, -1), 'R'))
        result = max(result, count_energized(puzzle_input, (row, len(puzzle_input[row])), 'L'))
    for col in range(len(puzzle_input[0])):
        result = max(result, count_energized(puzzle_input, (-1, col), 'D'))
        result = max(result, count_energized(puzzle_input, (len(puzzle_input), col), 'U'))
    return result


def solve(filename, solve_func):
    with open(f"data/{filename}", 'r') as input_file:
        puzzle_input = [line.replace('\n', '') for line in input_file.readlines()]
    return solve_func(puzzle_input)


if __name__ == '__main__':
    print(solve("day16.txt", first))
    print(solve("day16.txt", second))
