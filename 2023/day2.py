def first(filename):
    with open(f"2023/data/{filename}", 'r') as input_file:
        games = input_file.readlines()
    result = 0
    max_vals = {'red': 12, 'green': 13, 'blue': 14}
    for game in games:
        title, subsets = game.replace('\n', '').split(': ')
        number = int(title.split()[1])
        is_ok = True
        for subset in subsets.split('; '):
            for color in subset.split(', '):
                amount, color_name = color.split()
                if int(amount) > max_vals[color_name]:
                    is_ok = False
                    break
        if is_ok:
            result += number
    return result


def second(filename):
    with open(f"2023/data/{filename}", 'r') as input_file:
        games = input_file.readlines()
    result = 0
    for game in games:
        min_vals = {'red': 0, 'green': 0, 'blue': 0}
        title, subsets = game.replace('\n', '').split(': ')
        for subset in subsets.split('; '):
            for color in subset.split(', '):
                amount, color_name = color.split()
                min_vals[color_name] = max(min_vals[color_name], int(amount))
        result += min_vals['red'] * min_vals['green'] * min_vals['blue']
    return result


if __name__ == '__main__':
    print(first("day2.txt"))
    print(second("day2.txt"))
