def combination(source, target):
    dp = [[0 for _ in range(len(source))] for _ in range(len(target))]
    dp[0][0] = 1
    idx = 1
    while idx < len(source) and source[idx] != '#':
        dp[0][idx] = 1
        idx += 1
    for i in range(1, len(target)):
        for j in range(1, len(source)):
            if source[j] != target[i] and source[j] != '?':
                dp[i][j] = 0
            else:
                if target[i] == '.':
                    dp[i][j] = dp[i][j - 1] + dp[i - 1][j - 1]
                if target[i] == '#':
                    dp[i][j] = dp[i - 1][j - 1]
    return dp[len(target) - 1][len(source) - 1]


def first(filename):
    with open(f"data/{filename}", 'r') as input_file:
        puzzle_input = [line.replace('\n', '').split() for line in input_file.readlines()]
    result = 0
    for map_row, numbers in puzzle_input:
        target_row = f".{'.'.join(['#' * int(num) for num in numbers.split(',')])}."
        result += combination(f".{map_row}.", target_row)
    return result


def second(filename):
    with open(f"data/{filename}", 'r') as input_file:
        puzzle_input = [line.replace('\n', '').split() for line in input_file.readlines()]
    result = 0
    for map_row, numbers in puzzle_input:
        target_row = '.'.join(['#' * int(num) for num in numbers.split(',')])
        target_row = '.' + ((target_row + '.') * 5)
        map_row = (map_row + '?') * 5
        result += combination(f".{map_row[:-1]}.", target_row)
    return result


if __name__ == '__main__':
    print(first("day12.txt"))
    print(second("day12.txt"))
