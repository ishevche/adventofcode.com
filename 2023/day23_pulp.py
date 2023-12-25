import pandas as pd
import pulp
from pulp import LpProblem


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


def add_constraint(constraint: pulp.LpConstraint, lp_problem):
    if len(constraint.keys()) == 1:
        return
    lp_problem += constraint, f'{constraint}'


def max_distance(puzzle_input, start, end):
    key_points = {(x, y): {} for x in range(len(puzzle_input)) for y in range(len(puzzle_input[x]))
                  if is_intersection(puzzle_input, x, y) or (x, y) in [start, end]}
    for key in key_points.keys():
        fill_lengths(key, puzzle_input, key, key_points, 0)
    edges = [(start, end) for start in key_points.keys() for end in key_points[start].keys()]

    lp_problem = LpProblem("max_distance", sense=pulp.LpMaximize)

    edges_variables = pd.Series(edges).apply(
        lambda edge: pd.Series({
            "start": edge[0],
            "end": edge[1],
            "var": pulp.LpVariable(f"{edge[0]} to {edge[1]}", cat=pulp.LpBinary),
            "val": key_points[edge[0]][edge[1]]
        })
    )
    lp_problem.objective = edges_variables.apply(lambda row: row['var'] * row['val'], axis=1).sum()

    u_variables = pd.Series(key_points.keys()).apply(
        lambda vertex: pd.Series({
            "vertex": vertex,
            "var": pulp.LpVariable(f"u_{vertex}", lowBound=1, upBound=len(key_points), cat=pulp.LpInteger)
        })
    )
    u_variables.set_index("vertex", inplace=True, drop=True)

    edges_out = edges_variables.groupby("start")['var'].sum()
    edges_in: pd.Series = edges_variables.groupby("end")['var'].sum()
    constraints_out = edges_out.apply(lambda var: var <= 1)
    constraints_in = edges_in.apply(lambda var: var <= 1)
    constraints_in_out = pd.Series(list(set(key_points.keys()).difference([start, end]))).apply(
        lambda vertex: edges_out[vertex] == edges_in[vertex]
    )
    constraints_u = edges_variables.apply(
        lambda row: (u_variables['var'][row['start']] - u_variables['var'][row['end']] +
                     len(u_variables) * row['var'] <= len(u_variables) - 1),
        axis=1
    )
    constraints = pd.concat([constraints_out, constraints_in, constraints_in_out, constraints_u]).reset_index(drop=True)
    constraints.apply(lambda constraint: add_constraint(constraint, lp_problem))
    lp_problem += edges_out[start] == 1, 'start from start'

    lp_problem.solve()

    edges_variables['edge_val'] = edges_variables['var'].apply(lambda var: int(var.value()))

    path = [start]
    while path[-1] != end:
        path.append(edges_variables[(edges_variables['edge_val'] == 1) &
                                    (edges_variables['start'] == path[-1])]['end'].iloc[0])

    return edges_variables.apply(lambda row: row['edge_val'] * row['val'], axis=1).sum(), path


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
