import re


class Brick:
    def __init__(self, string):
        input_regex = re.compile(r'^(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)$')
        match = input_regex.match(string)
        if not match:
            raise ValueError
        x1, y1, z1, x2, y2, z2 = map(int, match.groups())
        self.x1, self.y1, self.z1 = min(x1, x2), min(y1, y2), min(z1, z2)
        self.x2, self.y2, self.z2 = max(x1, x2), max(y1, y2), max(z1, z2)
        self.under = set()
        self.on = set()

    def add_under(self, other):
        self.under.add(other)

    def __lt__(self, other):
        return self.z1 < other.z1


def compress(bricks):
    bricks.sort()
    x_min = min(bricks, key=lambda brick: brick.x1).x1
    x_max = max(bricks, key=lambda brick: brick.x2).x2
    y_min = min(bricks, key=lambda brick: brick.y1).y1
    y_max = max(bricks, key=lambda brick: brick.y2).y2
    width = x_max - x_min + 1
    depth = y_max - y_min + 1
    layout = [[(0, -1) for _ in range(depth)] for _ in range(width)]
    for brick in bricks:
        brick.x1 = brick.x1 - x_min
        brick.x2 = brick.x2 - x_min
        brick.y1 = brick.y1 - y_min
        brick.y2 = brick.y2 - y_min
    for idx, brick in enumerate(bricks):
        max_z = 0
        on = set()
        for x in range(brick.x1, brick.x2 + 1):
            for y in range(brick.y1, brick.y2 + 1):
                if layout[x][y][0] > max_z:
                    max_z = layout[x][y][0]
                    on = {layout[x][y][1]}
                elif layout[x][y][0] == max_z and layout[x][y][1] != -1:
                    on.add(layout[x][y][1])
        for brick_idx in on:
            bricks[brick_idx].add_under(idx)
        max_z += 1
        diff = brick.z1 - max_z
        brick.z1 -= diff
        brick.z2 -= diff
        brick.on = on
        for x in range(brick.x1, brick.x2 + 1):
            for y in range(brick.y1, brick.y2 + 1):
                layout[x][y] = brick.z2, idx


def first(bricks):
    result = 0
    for brick in bricks:
        is_good = True
        for on_brick in brick.under:
            if len(bricks[on_brick].on) == 1:
                is_good = False
                break
        result += int(is_good)
    return result


def second(bricks: list[Brick]):
    result = 0
    for idx, brick in enumerate(bricks):
        fallen = {idx}
        stack = [idx]
        while stack:
            fallen_brick = stack.pop()
            for cur_brick in bricks[fallen_brick].under:
                if len(bricks[cur_brick].on.difference(fallen)) == 0:
                    fallen.add(cur_brick)
                    stack.append(cur_brick)
        result += len(fallen) - 1
    return result


def solve(filename, solve_func):
    with open(f"data/{filename}", 'r') as input_file:
        puzzle_input = [Brick(line.replace('\n', '')) for line in input_file.readlines()]
    compress(puzzle_input)
    return solve_func(puzzle_input)


if __name__ == '__main__':
    print(solve("day22.txt", first))
    print(solve("day22.txt", second))
