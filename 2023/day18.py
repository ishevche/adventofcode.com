def dig(start, direction, length, terrain):
    x, y = start
    delta = None
    if direction == 'U':
        delta = (-1, 0)
    if direction == 'R':
        delta = (0, 1)
    if direction == 'D':
        delta = (1, 0)
    if direction == 'L':
        delta = (0, -1)
    for _ in range(length):
        x, y = x + delta[0], y + delta[1]
        terrain[x][y] = '_'
    return x, y


def fill(terrain, start):
    stack = [start]
    while stack:
        x, y = stack.pop()
        terrain[x][y] = '.'
        directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(terrain) and 0 <= ny < len(terrain[nx]) and terrain[nx][ny] == '#':
                stack.append((nx, ny))


def first(puzzle_input):
    min_x, max_x = 0, 0
    min_y, max_y = 0, 0
    cur_x, cur_y = 0, 0
    for line in puzzle_input:
        direction, number, _ = line.split()
        if direction == "U":
            cur_x -= int(number)
            min_x = min(min_x, cur_x)
        if direction == "R":
            cur_y += int(number)
            max_y = max(max_y, cur_y)
        if direction == "D":
            cur_x += int(number)
            max_x = max(max_x, cur_x)
        if direction == "L":
            cur_y -= int(number)
            min_y = min(min_y, cur_y)
    height = max_x - min_x + 1
    width = max_y - min_y + 1
    terrain = [['#' for _ in range(3 * width)] for _ in range(3 * height)]
    cur_x, cur_y = 1 - 3 * min_x, 1 - 3 * min_y
    terrain[cur_x][cur_y] = '_'
    for line in puzzle_input:
        direction, number, _ = line.split()
        cur_x, cur_y = dig((cur_x, cur_y), direction, int(number) * 3, terrain)
    fill(terrain, (0, 0))
    small_terrain = [[0 if terrain[3 * x + 1][3 * y + 1] == '.' else 1 for y in range(width)] for x in range(height)]
    return sum(map(sum, small_terrain))


def second(puzzle_input):
    min_x, max_x = 0, 0
    min_y, max_y = 0, 0
    cur_x, cur_y = 0, 0
    steps = []
    for line in puzzle_input:
        _, _, color = line.split()
        direction, number = color[-2], int(color[2:-2], 16)
        if direction == "3":
            cur_x -= number
            min_x = min(min_x, cur_x)
        if direction == "0":
            cur_y += number
            max_y = max(max_y, cur_y)
        if direction == "1":
            cur_x += number
            max_x = max(max_x, cur_x)
        if direction == "2":
            cur_y -= number
            min_y = min(min_y, cur_y)
        steps.append((int(direction), number))
    cur_x = -min_x
    result = 1
    for direction, number in steps:
        if direction == 3:
            cur_x -= number
        if direction == 0:
            result -= cur_x * number
        if direction == 1:
            cur_x += number
            result += number
        if direction == 2:
            result += (cur_x + 1) * number
    return result


def solve(filename, solve_func):
    with open(f"data/{filename}", 'r') as input_file:
        puzzle_input = [line.replace('\n', '') for line in input_file.readlines()]
    return solve_func(puzzle_input)


if __name__ == '__main__':
    print(solve("day18.txt", first))
    print(solve("day18.txt", second))
