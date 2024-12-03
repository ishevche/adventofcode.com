import re


def first(puzzle_input):
    s = 0
    reg = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
    for a, b in reg.findall(puzzle_input):
        s += int(a) * int(b)
    return s



def second(puzzle_input):
    reg = re.compile(r"(mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\))")
    s = 0
    active = True
    for cmd, a, b in reg.findall(puzzle_input):
        if cmd == "don't()":
            active = False
        elif cmd == "do()":
            active = True
        elif active:
            s += int(a) * int(b)
    return s


def solve(filename, solve_func):
    with open(f"data/{filename}", 'r') as input_file:
        puzzle_input = input_file.read()
    return solve_func(puzzle_input)


if __name__ == '__main__':
    print(solve("day03.txt", first))
    print(solve("day03.txt", second))
