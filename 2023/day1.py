def first(file):
    with open(f"2023/data/{file}", 'r') as input_file:
        calibrations = input_file.readlines()
    result = 0
    for calibration in calibrations:
        first_digit = next(s for s in calibration if s.isdigit())
        last_digit = next(s for s in reversed(calibration) if s.isdigit())
        result += int(first_digit + last_digit)
    return result


def starts_with(string, substrings):
    for substring in substrings:
        if string.startswith(substring):
            return substring


def second(file):
    with open(f"2023/data/{file}", 'r') as input_file:
        calibrations = input_file.readlines()
    result = 0
    passing_substrings = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                          'zero', 'one', 'two', 'three', 'four', 'five', 'six',
                          'seven', 'eight', 'nine', ]
    for calibration in calibrations:
        first_digit = (starts_with(calibration[idx:], passing_substrings)
                       for idx in range(len(calibration)))
        last_digit = (starts_with(calibration[idx:], passing_substrings)
                      for idx in reversed(range(len(calibration))))
        first_digit = next(passing_substrings.index(val) for val in first_digit
                           if val is not None) % 10
        last_digit = next(passing_substrings.index(val) for val in last_digit
                          if val is not None) % 10
        result += 10 * first_digit + last_digit
    return result


if __name__ == '__main__':
    print(first("day1.txt"))
    print(second("day1.txt"))
