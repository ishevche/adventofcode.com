def move_in_direction(direction, x, y):
    if direction == '^':
        return x - 1, y
    if direction == '>':
        return x, y + 1
    if direction == 'v':
        return x + 1, y
    if direction == '<':
        return x, y - 1


def is_intersection(layout, x, y):
    count = 0
    for direction in '^>v<':
        new_x, new_y = move_in_direction(direction, x, y)
        if (0 <= new_x < len(layout) and 0 <= new_y < len(layout[new_x]) and
                layout[new_x][new_y] != '#' and layout[x][y] != '#'):
            count += 1
    return count >= 3


def fill_lengths(start, layout, initial, key_points, cur_distance):
    prev = layout[start[0]][start[1]]
    layout[start[0]][start[1]] = '0'
    directions = '^>v<' if prev == '.' else prev
    for direction in directions:
        new_x, new_y = move_in_direction(direction, *start)
        if not (0 <= new_x < len(layout) and 0 <= new_y < len(layout[new_x])) or layout[new_x][new_y] in '0#':
            continue
        if (new_x, new_y) in key_points:
            key_points[initial][(new_x, new_y)] = cur_distance + 1
        else:
            fill_lengths((new_x, new_y), layout, initial, key_points, cur_distance + 1)
    layout[start[0]][start[1]] = prev


def max_path_in_graph(graph, src, dst, visited):
    if src == dst:
        return 0
    visited[src] = True
    max_dist = -1
    for neighbor, weight in graph[src].items():
        if not visited[neighbor]:
            next_dist = max_path_in_graph(graph, neighbor, dst, visited)
            if next_dist + weight > max_dist and next_dist != -1:
                max_dist = next_dist + weight
    visited[src] = False
    return max_dist


def max_distance(puzzle_input, start, end):
    key_points = {(x, y): {} for x in range(len(puzzle_input)) for y in range(len(puzzle_input[x]))
                  if is_intersection(puzzle_input, x, y) or (x, y) in [start, end]}
    for key in key_points.keys():
        fill_lengths(key, puzzle_input, key, key_points, 0)
    visited = {key: False for key in key_points.keys()}
    return max_path_in_graph(key_points, start, end, visited)


def first(puzzle_input):
    start_x = 0
    start_y = next(i for i, cell in enumerate(puzzle_input[start_x]) if cell in '.^>v<')
    end_x = len(puzzle_input) - 1
    end_y = next(i for i, cell in enumerate(puzzle_input[end_x]) if cell in '.^>v<')
    return max_distance(puzzle_input, (start_x, start_y), (end_x, end_y))


def second(puzzle_input):
    for row in range(len(puzzle_input)):
        for col in range(len(puzzle_input[row])):
            if puzzle_input[row][col] in '^>v<':
                puzzle_input[row][col] = '.'
    start_x = 0
    start_y = next(i for i, cell in enumerate(puzzle_input[start_x]) if cell in '.')
    end_x = len(puzzle_input) - 1
    end_y = next(i for i, cell in enumerate(puzzle_input[end_x]) if cell in '.')
    return max_distance(puzzle_input, (start_x, start_y), (end_x, end_y))


def solve(filename, solve_func):
    with open(f"data/{filename}", 'r') as input_file:
        puzzle_input = [list(line.replace('\n', '')) for line in input_file.readlines()]
    return solve_func(puzzle_input)


if __name__ == '__main__':
    print(solve("day23.txt", first))
    print(solve("day23.txt", second))
