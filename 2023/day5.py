import re


def first(filename):
    with open(f"data/{filename}", 'r') as input_file:
        puzzle_input = [line.replace('\n', '') for line in input_file.readlines()]
    _, seeds = puzzle_input[0].split(': ')
    seeds = map(int, seeds.split())
    data = [{'seed': seed} for seed in seeds]
    puzzle_input = puzzle_input[2:]
    while len(puzzle_input) != 0:
        regex = re.compile(r'^(\w*)-to-(\w*) map:$')
        src, dst = regex.findall(puzzle_input[0])[0]
        puzzle_input = puzzle_input[1:]
        ranges = []
        while puzzle_input and puzzle_input[0]:
            dst_start, src_start, length = map(int, puzzle_input[0].split())
            ranges += [((src_start, length), (dst_start, length))]
            puzzle_input = puzzle_input[1:]
        for seed_data in data:
            src_val = seed_data[src]
            for src_range, dst_range in ranges:
                if src_range[0] <= src_val < src_range[0] + src_range[1]:
                    seed_data[dst] = dst_range[0] + src_val - src_range[0]
                    break
            if dst not in seed_data:
                seed_data[dst] = src_val
        puzzle_input = puzzle_input[1:]
    return min(map(lambda x: x['location'], data))


def translate(seed_data, src, dst, src_range, dst_range, data):
    start, length = seed_data[src]
    if start >= src_range[0] + src_range[1] or start + length <= src_range[0]:
        return
    if start >= src_range[0]:
        dst_start = dst_range[0] + start - src_range[0]
        dst_length = min(length,  src_range[0] + src_range[1] - start)
        length_left = length - dst_length
        if length_left != 0:
            seed_data_copy = {}
            for key in seed_data.keys():
                seed_data[key] = seed_data[key][0], dst_length
                seed_data_copy[key] = seed_data[key][0] + dst_length, length_left
            data.append(seed_data_copy)
        seed_data[dst] = dst_start, dst_length
        return
    if start + length <= src_range[0] + src_range[1]:
        dst_start = dst_range[0]
        dst_length = length - src_range[0] + start
        length_left = length - dst_length

        seed_data_copy = {}
        for key in seed_data.keys():
            seed_data[key] = seed_data[key][0], length_left
            seed_data_copy[key] = seed_data[key][0] + length_left, dst_length
        seed_data_copy[dst] = dst_start, dst_length
        data.append(seed_data_copy)
        return

    dst_start = dst_range[0]
    dst_length = dst_range[1]
    before_left = src_range[0] - start
    after_left = start + length - src_range[0] - src_range[1]
    middle_copy = {}
    after_copy = {}
    for key in seed_data.keys():
        seed_data[key] = seed_data[key][0], before_left
        middle_copy[key] = seed_data[key][0] + before_left, dst_length
        after_copy[key] = seed_data[key][0] + before_left + dst_length, after_left
    middle_copy[dst] = dst_start, dst_length
    data.append(middle_copy)
    data.append(after_copy)

def second(filename):
    with open(f"data/{filename}", 'r') as input_file:
        puzzle_input = [line.replace('\n', '') for line in input_file.readlines()]
    _, seeds_ranges = puzzle_input[0].split(': ')
    seeds_ranges = list(map(int, seeds_ranges.split()))
    data = [{'seed': (start, length)} for start, length in zip(seeds_ranges[::2], seeds_ranges[1::2])]
    puzzle_input = puzzle_input[2:]
    while len(puzzle_input) != 0:
        regex = re.compile(r'^(\w*)-to-(\w*) map:$')
        src, dst = regex.findall(puzzle_input[0])[0]
        puzzle_input = puzzle_input[1:]
        ranges = []
        while puzzle_input and puzzle_input[0]:
            dst_start, src_start, length = map(int, puzzle_input[0].split())
            ranges += [((src_start, length), (dst_start, length))]
            puzzle_input = puzzle_input[1:]
        for seed_data in data:
            for src_range, dst_range in ranges:
                translate(seed_data, src, dst, src_range, dst_range, data)
        for seed_data in data:
            if dst not in seed_data:
                seed_data[dst] = seed_data[src]
        puzzle_input = puzzle_input[1:]
    return min(map(lambda x: x['location'][0], data))


if __name__ == '__main__':
    print(first("day5.txt"))
    print(second("day5.txt"))
