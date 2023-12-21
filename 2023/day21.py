import collections
import copy


def bfs(layout, start_position):
    layout[start_position[0]][start_position[1]] = 0
    q = collections.deque([start_position])
    while q:
        x, y = q.popleft()
        cur_path = layout[x][y]
        for dx, dy in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            if (0 <= x + dx < len(layout) and
                    0 <= y + dy < len(layout[x + dx]) and
                    layout[x + dx][y + dy] == '.'):
                layout[x + dx][y + dy] = cur_path + 1
                q.append((x + dx, y + dy))


def first(puzzle_input, start, steps):
    bfs(puzzle_input, start)
    result = 0
    for row in puzzle_input:
        for cell in row:
            if isinstance(cell, int) and cell <= steps and (steps - cell) % 2 == 0:
                result += 1
    return result


def calculate_amount(layout, steps_left, steps_between):
    result = 0
    for row in layout:
        for cell in row:
            if (isinstance(cell, int) and
                    cell <= steps_left and
                    (steps_left - cell) % 2 == 0):
                result += (steps_left - cell) // (2 * steps_between) + 1
            if (isinstance(cell, int) and
                    cell + steps_between <= steps_left and
                    (steps_left - cell - steps_between) % 2 == 0):
                result += (steps_left - cell - steps_between) // (2 * steps_between) + 1
    return result


def second(puzzle_input, start, steps):
    puzzle_input[start[0]][start[1]] = '.'
    grid = [[copy.deepcopy(puzzle_input) for _ in range(3)] for _ in range(3)]
    bfs(grid[1][1], start)
    center_amount = 0
    for row in grid[1][1]:
        for cell in row:
            if isinstance(cell, int) and cell <= steps and (steps - cell) % 2 == 0:
                center_amount += 1
    u_min = min(map(lambda x: grid[1][1][0][x], range(len(puzzle_input[0]))))
    d_min = min(map(lambda x: grid[1][1][-1][x], range(len(puzzle_input[0]))))
    l_min = min(map(lambda x: grid[1][1][x][0], range(len(puzzle_input))))
    r_min = min(map(lambda x: grid[1][1][x][-1], range(len(puzzle_input))))
    u_idx = next(i for i in range(len(puzzle_input[0])) if grid[1][1][0][i] == u_min)
    d_idx = next(i for i in range(len(puzzle_input[0])) if grid[1][1][-1][i] == d_min)
    l_idx = next(i for i in range(len(puzzle_input[0])) if grid[1][1][i][0] == l_min)
    r_idx = next(i for i in range(len(puzzle_input[0])) if grid[1][1][i][-1] == r_min)
    bfs(grid[1][0], (l_idx, len(puzzle_input[0]) - 1))
    bfs(grid[1][2], (r_idx, 0))
    bfs(grid[0][1], (len(puzzle_input) - 1, u_idx))
    bfs(grid[2][1], (0, d_idx))
    u_steps = min(map(lambda x: grid[0][1][0][x], range(len(puzzle_input[0]))))
    d_steps = min(map(lambda x: grid[2][1][-1][x], range(len(puzzle_input[0]))))
    l_steps = min(map(lambda x: grid[1][0][x][0], range(len(puzzle_input))))
    r_steps = min(map(lambda x: grid[1][2][x][-1], range(len(puzzle_input))))
    assert grid[0][1][0][u_idx] == u_steps
    assert grid[2][1][-1][d_idx] == d_steps
    assert grid[1][0][l_idx][0] == l_steps
    assert grid[1][2][r_idx][-1] == r_steps
    u_left = steps - u_min - 1
    d_left = steps - d_min - 1
    r_left = steps - r_min - 1
    l_left = steps - l_min - 1
    u_steps += 1
    d_steps += 1
    l_steps += 1
    r_steps += 1
    u_amount = calculate_amount(grid[0][1], u_left, u_steps)
    d_amount = calculate_amount(grid[2][1], d_left, d_steps)
    l_amount = calculate_amount(grid[1][0], l_left, l_steps)
    r_amount = calculate_amount(grid[1][2], r_left, r_steps)
    bfs(grid[0][0], (len(puzzle_input) - 1, len(puzzle_input[0]) - 1))
    bfs(grid[0][2], (len(puzzle_input) - 1, 0))
    bfs(grid[2][0], (0, len(puzzle_input[0]) - 1))
    bfs(grid[2][2], (0, 0))
    ul_left = steps - grid[1][1][0][0] - 2
    ur_left = steps - grid[1][1][0][-1] - 2
    dl_left = steps - grid[1][1][-1][0] - 2
    dr_left = steps - grid[1][1][-1][-1] - 2
    ul_steps = grid[0][0][0][-1] + 1
    ur_steps = grid[0][2][0][0] + 1
    dl_steps = grid[2][0][-1][-1] + 1
    dr_steps = grid[2][2][-1][0] + 1
    ul_amount = 0
    ur_amount = 0
    dl_amount = 0
    dr_amount = 0
    for steps_left in range(ul_left, -1, -grid[0][0][-1][0] - 1):
        ul_amount += calculate_amount(grid[0][0], steps_left, ul_steps)
    for steps_left in range(ur_left, -1, -grid[0][2][-1][-1] - 1):
        ur_amount += calculate_amount(grid[0][2], steps_left, ur_steps)
    for steps_left in range(dl_left, -1, -grid[2][0][0][0] - 1):
        dl_amount += calculate_amount(grid[2][0], steps_left, dl_steps)
    for steps_left in range(dr_left, -1, -grid[2][2][0][-1] - 1):
        dr_amount += calculate_amount(grid[2][2], steps_left, dr_steps)
    return center_amount + u_amount + d_amount + l_amount + r_amount + ul_amount + ur_amount + dl_amount + dr_amount


def solve(filename, solve_func, steps):
    with open(f"data/{filename}", 'r') as input_file:
        puzzle_input = [list(line.replace('\n', '')) for line in input_file.readlines()]
    start = None
    for row_idx, row in enumerate(puzzle_input):
        for col_idx, cell in enumerate(row):
            if cell == 'S':
                start = (row_idx, col_idx)
                break
        if start is not None: break
    return solve_func(puzzle_input, start, steps)


if __name__ == '__main__':
    print(solve("day21.txt", first, 64))
    print(solve("day21.txt", second, 26501365))
