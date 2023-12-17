import copy

directions_deltas = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def prev_coords_from_direction(x, y, direction):
    delta_x, delta_y = directions_deltas[direction]
    return x + delta_x, y + delta_y


def safe_get(arr, *args):
    cur = arr
    for idx in args:
        if 0 <= idx < len(cur):
            cur = cur[idx]
        else:
            return None
    return cur


def propagate(dp, puzzle_input, min_steps, max_steps):
    dp = copy.deepcopy(dp)
    for x in range(len(puzzle_input)):
        for y in range(len(puzzle_input[x])):
            for direction in range(4):
                for steps in range(max_steps):
                    if steps == 0:
                        prev_directions = ((direction + 3) % 4, (direction + 1) % 4)
                        min_val = float('inf')
                        for prev_direction in prev_directions:
                            prev_cell = safe_get(dp, *prev_coords_from_direction(x, y, prev_direction))
                            if prev_cell is None:
                                continue
                            for prev_steps in range(min_steps - 1, max_steps - 1):
                                min_val = min(min_val, prev_cell[prev_direction][prev_steps])
                        dp[x][y][direction][steps] = min(min_val + int(puzzle_input[x][y]), dp[x][y][direction][steps])
                    else:
                        prev_cell = safe_get(dp, *prev_coords_from_direction(x, y, direction))
                        if prev_cell is None:
                            continue
                        dp[x][y][direction][steps] = min(prev_cell[direction][steps - 1] + int(puzzle_input[x][y]),
                                                         dp[x][y][direction][steps])
    return dp


def solve(filename, min_steps, max_steps):
    with open(f"data/{filename}", 'r') as input_file:
        puzzle_input = [line.replace('\n', '') for line in input_file.readlines()]
    prev_dp = [[[[float('inf') for _ in range(max_steps)] for _ in range(4)]
                for _ in range(len(puzzle_input[0]))] for _ in range(len(puzzle_input))]
    prev_dp[0][0][0][0] = 0
    prev_dp[0][0][1][0] = 0
    prev_dp[0][0][2][0] = 0
    prev_dp[0][0][3][0] = 0
    new_dp = propagate(prev_dp, puzzle_input, min_steps, max_steps)
    cur_val = min(map(lambda steps: min(steps[min_steps:]), new_dp[-1][-1]))
    while new_dp != prev_dp:
        print(cur_val, end=', ')
        prev_dp = new_dp
        new_dp = propagate(prev_dp, puzzle_input, min_steps, max_steps)
        cur_val = min(map(lambda steps: min(steps[min_steps:]), new_dp[-1][-1]))
    return cur_val


if __name__ == '__main__':
    print(solve("day17.txt", 1, 4))
    print(solve("day17.txt", 4, 11))
