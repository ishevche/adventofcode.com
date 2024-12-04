import itertools


def matches(arr, word, start, direction, depth):
    if depth >= len(word):
        return True
    i, j = start[0] + direction[0] * depth, start[1] + direction[1] * depth
    if i < 0 or i >= len(arr) or \
            j < 0 or j >= len(arr[0]):
        return False
    if arr[i][j] == word[depth]:
        return matches(arr, word, start, direction, depth + 1)
    return False


def first(puzzle_input):
    word = list(map(list, puzzle_input))
    directions = [(1, 0), (1, 1), (0, 1), (-1, 1),
                  (-1, 0), (-1, -1), (0, -1), (1, -1)]
    count = 0
    for i, j in itertools.product(range(len(word)), range(len(word[0]))):
        for direction in directions:
            if matches(word, "XMAS", (i, j), direction, 0):
                count += 1
    return count


def second(puzzle_input):
    word = list(map(list, puzzle_input))
    count = 0
    directions = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
    for i, j in itertools.product(range(len(word)), range(len(word[0]))):
        for direction1, direction2 in itertools.combinations(directions, 2):
            di, dj = direction1[0] - direction2[0], direction1[1] - direction2[1]
            if matches(word, "MAS", (i, j), direction1, 0) and \
                    matches(word, "MAS", (i + di, j + dj), direction2, 0):
                count += 1
    return count


def solve(filename, solve_func):
    with open(f"data/{filename}", 'r') as input_file:
        puzzle_input = [line.replace('\n', '') for line in input_file.readlines()]
    return solve_func(puzzle_input)


if __name__ == '__main__':
    print(solve("day04.txt", first))
    print(solve("day04.txt", second))
