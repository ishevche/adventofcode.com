import re


def get_period_size(a):
    for length in range(1, 50000):
        if a[-length:] == a[-2 * length:-length]:
            return length


def first(filename):
    with open(f"data/{filename}", 'r') as input_file:
        puzzle_input = [line.replace('\n', '') for line in input_file.readlines()]
    instructions = puzzle_input[0]
    puzzle_input = puzzle_input[2:]
    regex = re.compile(r'^(\w{3}) = \((\w{3}), (\w{3})\)$')
    nodes = {}
    for node in puzzle_input:
        origin, left, right = regex.findall(node)[0]
        nodes[origin] = left, right
    cur = 'AAA'
    instruction_idx = 0
    while cur != 'ZZZ':
        if instructions[instruction_idx % len(instructions)] == 'L':
            cur = nodes[cur][0]
        else:
            cur = nodes[cur][1]
        instruction_idx += 1
    return instruction_idx


def second(filename):
    with open(f"data/{filename}", 'r') as input_file:
        puzzle_input = [line.replace('\n', '') for line in input_file.readlines()]
    instructions = puzzle_input[0]
    puzzle_input = puzzle_input[2:]
    regex = re.compile(r'^(\w{3}) = \((\w{3}), (\w{3})\)$')
    nodes = {}
    for node in puzzle_input:
        origin, left, right = regex.findall(node)[0]
        nodes[origin] = left, right
    starts = [node for node in nodes.keys() if node[-1] == 'A']
    paths = [[] for _ in range(len(starts))]

    for idx, cur in enumerate(starts):
        instruction_idx = 0
        paths[idx] = [cur]
        while instruction_idx < 100000:
            if instructions[instruction_idx % len(instructions)] == 'L':
                cur = nodes[cur][0]
            else:
                cur = nodes[cur][1]
            instruction_idx += 1
            paths[idx].append(cur)
    return [get_period_size(path) for path in paths]


if __name__ == '__main__':
    print(first("day8.txt"))
    vals = second("day8.txt")
    result = 1
    for val in vals:
        result *= val / 269
    print(int(result * 269))
