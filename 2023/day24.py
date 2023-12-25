import itertools
import re
import sympy
import numpy as np


class Line:
    def __init__(self, string):
        regex = re.compile(r'^(-?\d+),\s+(-?\d+),\s+(-?\d+)\s+@\s+(-?\d+),\s+(-?\d+),\s+(-?\d+)$')
        self.px, self.py, self.pz, self.vx, self.vy, self.vz = map(int, regex.match(string).groups())

    def intersection2d(self, other):
        if not isinstance(other, Line):
            raise TypeError('Line must be of type Line')
        denominator = other.vy * self.vx - self.vy * other.vx
        if denominator == 0:
            return float('inf'), float('inf')
        t1 = (self.py - other.py) * other.vx - (self.px - other.px) * other.vy
        t2 = (self.py - other.py) * self.vx - (self.px - other.px) * self.vy
        t1 /= denominator
        t2 /= denominator
        return t1, t2

    def at(self, t):
        return (self.px + t * self.vx,
                self.py + t * self.vy,
                self.pz + t * self.vz)

    def __str__(self):
        return f'{self.px}, {self.py}, {self.pz} @ {self.vx}, {self.vy}, {self.vz}'


def first(puzzle_input):
    left_bound, right_bound = 200000000000000, 400000000000000
    result = 0
    for a, b in itertools.combinations(puzzle_input, 2):
        t1, t2 = a.intersection2d(b)
        if t1 < 0 or t2 < 0 or t1 == float('inf'):
            continue
        px, py, _ = a.at(t1)
        if left_bound <= px <= right_bound and left_bound <= py <= right_bound:
            result += 1
    return result


def second(puzzle_input):
    px, py, pz = sympy.symbols('px py pz')
    vx, vy, vz = sympy.symbols('vx vy vz')
    ts = []
    equations = []
    for idx in range(3):
        t = sympy.Symbol(f't{idx}')
        ts.append(t)
        line = puzzle_input[idx]
        equations.append(sympy.Eq(px + vx * t, line.px + line.vx * t))
        equations.append(sympy.Eq(py + vy * t, line.py + line.vy * t))
        equations.append(sympy.Eq(pz + vz * t, line.pz + line.vz * t))
    result = list(sympy.nonlinsolve(equations, px, py, pz, vx, vy, vz, *ts))[0]
    return result[0] + result[1] + result[2]


def solve(filename, solve_func):
    with open(f"data/{filename}", 'r') as input_file:
        puzzle_input = [Line(line.replace('\n', '')) for line in input_file.readlines()]
    return solve_func(puzzle_input)


if __name__ == '__main__':
    print(solve("day24.txt", first))
    print(solve("day24.txt", second))
