import itertools
import math

import numpy as np


def process_data(puzzle_input):
    split = [list(group) for k, group in itertools.groupby(puzzle_input, lambda x: x == '') if not k]
    for pattern in split:
        pattern = [list(row) for row in pattern]
        np_pattern = np.array(pattern)
        np_pattern = (np_pattern == '#').astype(int)
        row_powers = 2 ** np.arange(np_pattern.shape[1])
        col_powers = 2 ** np.arange(np_pattern.shape[0])
        rows = np.asmatrix(np_pattern) @ np.asmatrix(row_powers).T
        cols = np.asmatrix(np_pattern).T @ np.asmatrix(col_powers).T
        yield rows.T.A[0], cols.T.A[0]


def get_palindrome_idx1(lst):
    for i in range(len(lst) - 1):
        is_ok = True
        for j in range(min(i + 1, len(lst) - i - 1)):
            if lst[i - j] != lst[i + j + 1]:
                is_ok = False
                break
        if is_ok:
            return i
    return -1


def get_palindrome_idx2(lst):
    for i in range(len(lst) - 1):
        is_ok = True
        has_smudge = False
        for j in range(min(i + 1, len(lst) - i - 1)):
            if lst[i - j] != lst[i + j + 1]:
                diff = abs(lst[i + j + 1] - lst[i - j])
                if 2 ** int(math.log2(diff)) == diff and not has_smudge:
                    has_smudge = True
                else:
                    is_ok = False
                    break
        if is_ok and has_smudge:
            return i
    return -1


def solve(filename, solve_func):
    with open(f"data/{filename}", 'r') as input_file:
        puzzle_input = [line.replace('\n', '') for line in input_file.readlines()]
    result = 0
    for rows, cols in process_data(puzzle_input):
        rows_num = solve_func(rows)
        cols_num = solve_func(cols)
        if rows_num != -1:
            result += (rows_num + 1) * 100
        elif cols_num != -1:
            result += cols_num + 1
    return result


if __name__ == '__main__':
    print(solve("day13.txt", get_palindrome_idx1))
    print(solve("day13.txt", get_palindrome_idx2))
