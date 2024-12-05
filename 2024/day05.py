def parse_input(puzzle_input):
    graph = {}
    updates = []
    for line in puzzle_input:
        if '|' in line:
            u, v = map(int, line.split('|'))
            if v not in graph:
                graph[v] = set()
            graph[v].add(u)
        elif line != '':
            updates.append(list(map(int, line.split(','))))
    return graph, updates


def topologically_sort(elements, graph):
    visited = set()
    result = []

    def dfs(v):
        if v in visited: return
        for neighbor in graph[v].intersection(elements):
            dfs(neighbor)
        visited.add(v)
        result.append(v)

    for node in elements:
        if node not in visited:
            dfs(node)
    return result


def first(update, sorted_update):
    return update == sorted_update


def second(update, sorted_update):
    return update != sorted_update


def solve(filename, solve_func):
    with open(f"data/{filename}", 'r') as input_file:
        puzzle_input = [line.replace('\n', '') for line in input_file.readlines()]
    graph, updates = parse_input(puzzle_input)
    # if the original update equals the topologically sorted update, it is definitely sorted
    # as topological sort is not unique it might not work in all cases
    sorted_updates = list(map(lambda update: topologically_sort(set(update), graph), updates))
    return sum(map(
        lambda upd_pair: upd_pair[1][len(upd_pair[1]) // 2],  # get the center element of the sorted update
        filter(
            lambda upd_pair: solve_func(upd_pair[0], upd_pair[1]),  # filters out the corresponding items
            zip(updates, sorted_updates) # list of pairs (original and sorted solutions)
        )
    ))


if __name__ == '__main__':
    print(solve("day05.txt", first))
    print(solve("day05.txt", second))
