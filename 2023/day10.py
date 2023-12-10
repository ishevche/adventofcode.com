N = 0b1000
E = 0b0100
S = 0b0010
W = 0b0001

letter_to_pipe = {
    '|': N | S,
    '-': E | W,
    'L': N | E,
    'J': N | W,
    'F': S | E,
    '7': S | W,
    '.': 0,
}


def get_adjacent(grid, pos):
    pipe = letter_to_pipe[grid[pos[0]][pos[1]]]
    result = []
    if pipe & N:
        result.append((pos[0] - 1, pos[1]))
    if pipe & E:
        result.append((pos[0], pos[1] + 1))
    if pipe & S:
        result.append((pos[0] + 1, pos[1]))
    if pipe & W:
        result.append((pos[0], pos[1] - 1))
    return tuple(result)


def get_start_pos(puzzle_input):
    start_pos = None
    for row_idx, row in enumerate(puzzle_input):
        for col_idx, char in enumerate(row):
            if char == 'S':
                start_pos = (row_idx, col_idx)
                break
        if start_pos is not None:
            break
    start_pipe = 0
    if letter_to_pipe[puzzle_input[start_pos[0] - 1][start_pos[1]]] & S: start_pipe |= N
    if letter_to_pipe[puzzle_input[start_pos[0] + 1][start_pos[1]]] & N: start_pipe |= S
    if letter_to_pipe[puzzle_input[start_pos[0]][start_pos[1] + 1]] & W: start_pipe |= E
    if letter_to_pipe[puzzle_input[start_pos[0]][start_pos[1] - 1]] & E: start_pipe |= W
    start_pipe_letter = list(letter_to_pipe.keys())[list(letter_to_pipe.values()).index(start_pipe)]
    puzzle_input[start_pos[0]] = puzzle_input[start_pos[0]].replace('S', start_pipe_letter)
    return start_pos


def first(filename):
    with open(f"data/{filename}", 'r') as input_file:
        puzzle_input = [line.replace('\n', '') for line in input_file.readlines()]

    start_pos = get_start_pos(puzzle_input)
    start_neighbors = get_adjacent(puzzle_input, start_pos)
    prev_pos = start_pos
    cur_pos = start_neighbors[0]
    steps = 1
    while cur_pos != start_pos:
        next_poses = get_adjacent(puzzle_input, cur_pos)
        if next_poses[0] == prev_pos:
            next_pos = next_poses[1]
        else:
            next_pos = next_poses[0]
        prev_pos = cur_pos
        cur_pos = next_pos
        steps += 1
    return int(steps / 2)


def mark_pipe(grid, position, pipe_type):
    center_x = position[0] * 3 + 1
    center_y = position[1] * 3 + 1
    grid[center_x][center_y] = 'P'
    pipe = letter_to_pipe[pipe_type]
    if pipe & N:
        grid[center_x - 1][center_y] = 'P'
    if pipe & E:
        grid[center_x][center_y + 1] = 'P'
    if pipe & S:
        grid[center_x + 1][center_y] = 'P'
    if pipe & W:
        grid[center_x][center_y - 1] = 'P'


def propagate_outside(grid, start_pos):
    stack = [start_pos]
    while stack:
        pos = stack.pop()
        grid[pos[0]][pos[1]] = 'O'
        displacements = ((0, 1), (1, 0), (0, -1), (-1, 0))
        for dx, dy in displacements:
            if 0 <= pos[0] + dx < len(grid) and 0 <= pos[1] + dy < len(grid[pos[0] + dx]):
                if grid[pos[0] + dx][pos[1] + dy] == 'I':
                    stack.append((pos[0] + dx, pos[1] + dy))


def second(filename):
    with open(f"data/{filename}", 'r') as input_file:
        puzzle_input = [line.replace('\n', '') for line in input_file.readlines()]
    start_pos = get_start_pos(puzzle_input)
    grid = [['I' for _ in range(3 * len(puzzle_input[0]))] for _ in range(3 * len(puzzle_input))]
    start_neighbors = get_adjacent(puzzle_input, start_pos)
    prev_pos = start_pos
    cur_pos = start_neighbors[0]
    mark_pipe(grid, cur_pos, puzzle_input[cur_pos[0]][cur_pos[1]])
    while cur_pos != start_pos:
        next_poses = get_adjacent(puzzle_input, cur_pos)
        if next_poses[0] == prev_pos:
            next_pos = next_poses[1]
        else:
            next_pos = next_poses[0]
        prev_pos = cur_pos
        cur_pos = next_pos
        mark_pipe(grid, cur_pos, puzzle_input[cur_pos[0]][cur_pos[1]])
    propagate_outside(grid, (0, 0))
    inside_counter = 0
    for row_idx in range(len(puzzle_input)):
        for col_idx in range(len(puzzle_input[row_idx])):
            if grid[row_idx * 3 + 1][col_idx * 3 + 1] == 'I':
                inside_counter += 1
    return inside_counter


if __name__ == '__main__':
    print(first("day10.txt"))
    print(second("day10.txt"))
