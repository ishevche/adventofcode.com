def first(puzzle_input):
    loc1 = []
    loc2 = []
    for line in puzzle_input:
        x, y = line.split()
        loc1.append(int(x))
        loc2.append(int(y))
    loc1.sort()
    loc2.sort()
    dist = 0
    for i in range(len(loc1)):
        dist += abs(loc1[i] - loc2[i])
    return dist


def second(puzzle_input):
    loc1 = []
    loc2 = []
    for line in puzzle_input:
        x, y = line.split()
        loc1.append(int(x))
        loc2.append(int(y))
    sim = 0
    for i in range(len(loc1)):
        sim += loc2.count(loc1[i]) * loc1[i]
    return sim


def solve(filename, solve_func):
    with open(f"data/{filename}", 'r') as input_file:
        puzzle_input = [line.replace('\n', '') for line in input_file.readlines()]
    return solve_func(puzzle_input)


if __name__ == '__main__':
    print(solve("day01.txt", first))
    print(solve("day01.txt", second))
