def symbol_type(char: str):
    if char.isdigit(): return 'd'
    if char == '.': return '.'
    return 's'


def get_or_none(data, i, j):
    if i < 0 or j < 0 or i >= len(data) or j >= len(data[0]):
        return None
    return data[i][j]


def has_adjacent_symbol(data, row_idx, col_idx):
    return (get_or_none(data, row_idx - 1, col_idx - 1) == 's' or
            get_or_none(data, row_idx - 1, col_idx) == 's' or
            get_or_none(data, row_idx - 1, col_idx + 1) == 's' or
            get_or_none(data, row_idx, col_idx - 1) == 's' or
            get_or_none(data, row_idx, col_idx + 1) == 's' or
            get_or_none(data, row_idx + 1, col_idx - 1) == 's' or
            get_or_none(data, row_idx + 1, col_idx) == 's' or
            get_or_none(data, row_idx + 1, col_idx + 1) == 's')


def get_gear_coords(grid, row_idx, col_idx):
    if get_or_none(grid, row_idx - 1, col_idx - 1) == '*': return row_idx - 1, col_idx - 1
    if get_or_none(grid, row_idx - 1, col_idx) == '*': return row_idx - 1, col_idx
    if get_or_none(grid, row_idx - 1, col_idx + 1) == '*': return row_idx - 1, col_idx + 1
    if get_or_none(grid, row_idx, col_idx - 1) == '*': return row_idx, col_idx - 1
    if get_or_none(grid, row_idx, col_idx + 1) == '*': return row_idx, col_idx + 1
    if get_or_none(grid, row_idx + 1, col_idx - 1) == '*': return row_idx + 1, col_idx - 1
    if get_or_none(grid, row_idx + 1, col_idx) == '*': return row_idx + 1, col_idx
    if get_or_none(grid, row_idx + 1, col_idx + 1) == '*': return row_idx + 1, col_idx + 1
    return False


def first(filename):
    with open(f"data/{filename}", 'r') as input_file:
        grid = [line.replace('\n', '') for line in input_file.readlines()]
    data = [[symbol_type(cell) for cell in row] for row in grid]
    result = 0
    for row_idx, row in enumerate(data):
        for col_idx, cell in enumerate(row):
            if cell != 'd':
                continue
            number = int(grid[row_idx][col_idx])
            has_symbol = has_adjacent_symbol(data, row_idx, col_idx)
            cur_idx = col_idx + 1
            while cur_idx < len(row) and row[cur_idx] == 'd':
                number *= 10
                number += int(grid[row_idx][cur_idx])
                has_symbol = has_symbol or has_adjacent_symbol(data, row_idx, cur_idx)
                row[cur_idx] = '.'
                cur_idx += 1
            if has_symbol:
                result += number
    return result


def second(filename):
    with open(f"data/{filename}", 'r') as input_file:
        grid = [line.replace('\n', '') for line in input_file.readlines()]
    data = [[symbol_type(cell) for cell in row] for row in grid]
    gears = {}
    for row_idx, row in enumerate(data):
        for col_idx, cell in enumerate(row):
            if cell != 'd':
                continue
            number = int(grid[row_idx][col_idx])
            gear_coords = get_gear_coords(grid, row_idx, col_idx)
            cur_idx = col_idx + 1
            while cur_idx < len(row) and row[cur_idx] == 'd':
                number *= 10
                number += int(grid[row_idx][cur_idx])
                if not gear_coords:
                    gear_coords = get_gear_coords(grid, row_idx, cur_idx)
                row[cur_idx] = '.'
                cur_idx += 1
            if gear_coords:
                if gear_coords in gears:
                    gears[gear_coords].append(number)
                else:
                    gears[gear_coords] = [number]
    result = 0
    for numbers in gears.values():
        if len(numbers) != 2:
            continue
        result += numbers[0] * numbers[1]
    return result


if __name__ == '__main__':
    print(first("day3.txt"))
    print(second("day3.txt"))
