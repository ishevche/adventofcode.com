import copy


def first(puzzle_input):
    roll(puzzle_input, 'N')
    return count_weight(puzzle_input)


def second(puzzle_input):
    prev = [puzzle_input]
    steps_to_do = 0
    for idx in range(1000000000):
        cur = roll_round(prev[-1])
        if idx % 100 == 99:
            rep_idx = -1
            for prev_idx, prev_platform in reversed(list(enumerate(prev))):
                if prev_platform == cur:
                    rep_idx = prev_idx
                    break
            if rep_idx != -1:
                steps_to_do = (1000000000 - idx) % (idx - rep_idx + 1)
                break
        prev.append(cur)
    prev = prev[-1]
    for _ in range(steps_to_do):
        cur = roll_round(prev)
        prev = cur
    return count_weight(prev)


def count_weight(puzzle_input):
    result = 0
    for row_idx, row in enumerate(reversed(puzzle_input)):
        for rock in row:
            if rock == 'O':
                result += row_idx + 1
    return result


def roll_round(platform):
    result = copy.deepcopy(platform)
    roll(result, 'N')
    roll(result, 'W')
    roll(result, 'S')
    roll(result, 'E')
    return result


def roll(puzzle_input, direction):
    if direction == 'N' or direction == 'S':
        for first_index in range(len(puzzle_input[0])):
            cur_free_place = 0 if direction == 'N' else len(puzzle_input) - 1
            adder = 1 if direction == 'N' else -1
            second_range = range(len(puzzle_input))
            if direction != 'N':
                second_range = reversed(second_range)
            for second_index in second_range:
                if puzzle_input[second_index][first_index] == '#':
                    cur_free_place = second_index + adder
                elif puzzle_input[second_index][first_index] == 'O':
                    puzzle_input[second_index][first_index] = '.'
                    puzzle_input[cur_free_place][first_index] = 'O'
                    cur_free_place += adder
    else:
        for first_index in range(len(puzzle_input)):
            cur_free_place = 0 if direction == 'W' else len(puzzle_input[0]) - 1
            adder = 1 if direction == 'W' else -1
            second_range = range(len(puzzle_input[0]))
            if direction != 'W':
                second_range = reversed(second_range)
            for second_index in second_range:
                if puzzle_input[first_index][second_index] == '#':
                    cur_free_place = second_index + adder
                elif puzzle_input[first_index][second_index] == 'O':
                    puzzle_input[first_index][second_index] = '.'
                    puzzle_input[first_index][cur_free_place] = 'O'
                    cur_free_place += adder


def solve(filename, solve_func):
    with open(f"data/{filename}", 'r') as input_file:
        puzzle_input = [list(line.replace('\n', '')) for line in input_file.readlines()]
    return solve_func(puzzle_input)


if __name__ == '__main__':
    print(solve("day14.txt", first))
    print(solve("day14.txt", second))
