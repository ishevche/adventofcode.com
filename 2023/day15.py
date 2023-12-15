def my_hash(string):
    cur_val = 0
    for c in string:
        cur_val += ord(c)
        cur_val *= 17
        cur_val %= 256
    return cur_val


def first(instructions):
    return sum(map(my_hash, instructions))


class Lenz:
    def __init__(self, label, focal_length):
        self.label = label
        self.focal_length = focal_length

    def __ne__(self, other):
        return not self == other

    def __eq__(self, other):
        if isinstance(other, Lenz):
            return self.label == other.label
        if isinstance(other, str):
            return self.label == other
        return False

    def __repr__(self):
        return f"[{self.label} {self.focal_length}]"


def second(instructions):
    boxes: dict[int, list] = {}
    for instruction in instructions:
        if instruction[-1] == '-':
            box = my_hash(instruction[:-1])
            if box in boxes:
                boxes[box] = list(filter(lambda x: x != instruction[:-1], boxes[box]))
        else:
            name, length = instruction.split('=')
            box = my_hash(name)
            if box not in boxes:
                boxes[box] = []
            new_lenz = Lenz(name, int(length))
            if new_lenz in boxes[box]:
                idx = boxes[box].index(new_lenz)
                boxes[box][idx] = new_lenz
            else:
                boxes[box].append(new_lenz)
    result = 0
    for box, content in boxes.items():
        for idx, lenz in enumerate(content):
            result += (1 + box) * (1 + idx) * lenz.focal_length
    return result


def solve(filename, solve_func):
    with open(f"data/{filename}", 'r') as input_file:
        puzzle_input = [line.replace('\n', '') for line in input_file.readlines()]
    return solve_func(puzzle_input[0].split(','))


if __name__ == '__main__':
    print(solve("day15.txt", first))
    print(solve("day15.txt", second))
