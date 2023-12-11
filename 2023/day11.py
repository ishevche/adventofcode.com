import itertools


def first(filename):
    with open(f"data/{filename}", 'r') as input_file:
        puzzle_input = [list(line.replace('\n', '')) for line in input_file.readlines()]
    rows = []
    cols = []
    for idx, row in enumerate(puzzle_input):
        if '#' not in row:
            rows.append(idx)
    for idx in range(len(puzzle_input[0])):
        present = False
        for row in puzzle_input:
            if row[idx] == '#':
                present = True
                break
        if not present:
            cols.append(idx)
    for idx in reversed(rows):
        puzzle_input.insert(idx, ['.' for _ in range(len(puzzle_input[0]))])
    for idx in reversed(cols):
        for row in puzzle_input:
            row.insert(idx, '.')

    galaxies = []
    for row_idx, row in enumerate(puzzle_input):
        for col_idx, cell in enumerate(row):
            if cell == '#':
                galaxies.append((row_idx, col_idx))
    result = 0
    for a, b in itertools.combinations(galaxies, 2):
        result += abs(a[0] - b[0]) + abs(a[1] - b[1])
    return result


def distance(dst, src, rows, cols, times):
    rows_to_add = 0
    for row in rows:
        if dst[0] <= row <= src[0] or src[0] <= row <= dst[0]:
            rows_to_add += 1
    for col in cols:
        if dst[1] <= col <= src[1] or src[1] <= col <= dst[1]:
            rows_to_add += 1
    return abs(dst[0] - src[0]) + abs(dst[1] - src[1]) + rows_to_add * (times - 1)



def second(filename):
    with open(f"data/{filename}", 'r') as input_file:
        puzzle_input = [list(line.replace('\n', '')) for line in input_file.readlines()]
    rows = []
    cols = []
    for idx, row in enumerate(puzzle_input):
        if '#' not in row:
            rows.append(idx)
    for idx in range(len(puzzle_input[0])):
        present = False
        for row in puzzle_input:
            if row[idx] == '#':
                present = True
                break
        if not present:
            cols.append(idx)

    galaxies = []
    for row_idx, row in enumerate(puzzle_input):
        for col_idx, cell in enumerate(row):
            if cell == '#':
                galaxies.append((row_idx, col_idx))
    result = 0
    for a, b in itertools.combinations(galaxies, 2):
        result += distance(a, b, rows, cols, 1000000)
    return result


if __name__ == '__main__':
    print(first("day11.txt"))
    print(second("day11.txt"))
