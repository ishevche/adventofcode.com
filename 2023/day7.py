class MyComparator(tuple):
    def __lt__(self, other):
        return compare(self[0], other[0])


def compare(hand1, hand2) -> bool:
    cards = "AKQJT98765432"

    def compare_by_letters():
        first_dif = 0
        while hand1[first_dif] == hand2[first_dif]: first_dif += 1
        return cards.index(hand1[first_dif]) > cards.index(hand2[first_dif])

    h1_occurrence = list(reversed(sorted([hand1.count(letter) for letter in cards if hand1.count(letter) != 0])))
    h2_occurrence = list(reversed(sorted([hand2.count(letter) for letter in cards if hand2.count(letter) != 0])))

    if h1_occurrence[0] == 5:
        if h2_occurrence[0] == 5:
            return compare_by_letters()
        return False
    elif h2_occurrence[0] == 5:
        return True

    if h1_occurrence[0] == 4:
        if h2_occurrence[0] == 4:
            return compare_by_letters()
        return False
    elif h2_occurrence[0] == 4:
        return True

    if h1_occurrence[0] == 3 and h1_occurrence[1] == 2:
        if h2_occurrence[0] == 3 and h2_occurrence[1] == 2:
            return compare_by_letters()
        return False
    elif h2_occurrence[0] == 3 and h2_occurrence[1] == 2:
        return True

    if h1_occurrence[0] == 3:
        if h2_occurrence[0] == 3:
            return compare_by_letters()
        return False
    elif h2_occurrence[0] == 3:
        return True

    if h1_occurrence[0] == 2 and h1_occurrence[1] == 2:
        if h2_occurrence[0] == 2 and h2_occurrence[1] == 2:
            return compare_by_letters()
        return False
    elif h2_occurrence[0] == 2 and h2_occurrence[1] == 2:
        return True

    if h1_occurrence[0] == 2:
        if h2_occurrence[0] == 2:
            return compare_by_letters()
        return False
    elif h2_occurrence[0] == 2:
        return True

    return compare_by_letters()


def first(filename):
    with open(f"data/{filename}", 'r') as input_file:
        puzzle_input = [line.replace('\n', '') for line in input_file.readlines()]
    data = list(map(lambda x: (x.split()[0], int(x.split()[1])), puzzle_input))
    data.sort(key=MyComparator)
    result = 0
    for idx, point in enumerate(data, start=1):
        result += idx * point[1]
    return result


class MyComparator2(tuple):
    def __lt__(self, other):
        return compare2(self[0], other[0])


def compare2(hand1, hand2) -> bool:
    cards = "AKQT98765432J"

    def compare_by_letters():
        first_dif = 0
        while hand1[first_dif] == hand2[first_dif]: first_dif += 1
        return cards.index(hand1[first_dif]) > cards.index(hand2[first_dif])

    h1_occurrence = list(reversed(sorted([hand1.count(letter) for letter in cards
                                          if letter != 'J' and hand1.count(letter) != 0])))
    h2_occurrence = list(reversed(sorted([hand2.count(letter) for letter in cards
                                          if letter != 'J' and hand2.count(letter) != 0])))
    jokers1 = hand1.count('J')
    jokers2 = hand2.count('J')
    if not h1_occurrence or h1_occurrence[0] + jokers1 == 5:
        if not h2_occurrence or h2_occurrence[0] + jokers2 == 5:
            return compare_by_letters()
        return False
    elif not h2_occurrence or h2_occurrence[0] + jokers2 == 5:
        return True

    if h1_occurrence[0] + jokers1 == 4:
        if h2_occurrence[0] + jokers2 == 4:
            return compare_by_letters()
        return False
    elif h2_occurrence[0] + jokers2 == 4:
        return True

    if h1_occurrence[0] + jokers1 == 3 and h1_occurrence[1] == 2:
        if h2_occurrence[0] + jokers2 == 3 and h2_occurrence[1] == 2:
            return compare_by_letters()
        return False
    elif h2_occurrence[0] + jokers2 == 3 and h2_occurrence[1] == 2:
        return True

    if h1_occurrence[0] + jokers1 == 3:
        if h2_occurrence[0] + jokers2 == 3:
            return compare_by_letters()
        return False
    elif h2_occurrence[0] + jokers2 == 3:
        return True

    if h1_occurrence[0] + jokers1 == 2 and h1_occurrence[1] == 2:
        if h2_occurrence[0] + jokers2 == 2 and h2_occurrence[1] == 2:
            return compare_by_letters()
        return False
    elif h2_occurrence[0] + jokers2 == 2 and h2_occurrence[1] == 2:
        return True

    if h1_occurrence[0] + jokers1 == 2:
        if h2_occurrence[0] + jokers2 == 2:
            return compare_by_letters()
        return False
    elif h2_occurrence[0] + jokers2 == 2:
        return True

    return compare_by_letters()


def second(filename):
    with open(f"data/{filename}", 'r') as input_file:
        puzzle_input = [line.replace('\n', '') for line in input_file.readlines()]
    data = list(map(lambda x: (x.split()[0], int(x.split()[1])), puzzle_input))
    data.sort(key=MyComparator2)
    result = 0
    for idx, point in enumerate(data, start=1):
        result += idx * point[1]
    return result


if __name__ == '__main__':
    print(first("day7.txt"))
    print(second("day7.txt"))
