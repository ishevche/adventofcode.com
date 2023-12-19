import re

import pandas as pd


def process(row, rules):
    if row.rule == 'A' or row.rule == 'R':
        return row.rule
    rule = rules[row.rule]
    for condition, next_rule in rule:
        if condition is None:
            return next_rule
        if eval(f'row.{condition}'):
            return next_rule


def first(rules, parts):
    parts = parts.copy()
    parts['rule'] = 'in'
    while not ((parts['rule'] == 'A') | (parts['rule'] == 'R')).all():
        parts['rule'] = parts.apply(lambda row: process(row, rules), axis=1)
    return parts[parts['rule'] == 'A'].sum()[['x', 'm', 'a', 's']].sum()


def process_range(row, rules):
    if row.rule == 'A' or row.rule == 'R':
        return row.to_frame().transpose()
    rule = rules[row.rule]
    result = pd.DataFrame(columns=['x', 'm', 'a', 's', 'rule'])
    for condition, next_rule in rule[:-1]:
        variable = condition[0]
        bigger = condition[1] == '>'
        smaller = condition[1] == '<'
        assert bigger or smaller
        value = int(condition[2:])
        range_start, range_end = row[variable]
        if bigger:
            row_copy = row.copy()
            row_copy[variable] = (value + 1, range_end)
            row_copy.rule = next_rule
            result.loc[len(result)] = row_copy
            row[variable] = (range_start, value + 1)
        if smaller:
            row_copy = row.copy()
            row_copy[variable] = (range_start, value)
            row_copy.rule = next_rule
            result.loc[len(result)] = row_copy
            row[variable] = (value, range_end)
    row.rule = rule[-1][1]
    result.loc[len(result)] = row
    return result


def second(rules, _):
    parts = pd.DataFrame({
        'x': [(1, 4001)],
        'm': [(1, 4001)],
        'a': [(1, 4001)],
        's': [(1, 4001)],
        'rule': 'in'
    })
    while not ((parts['rule'] == 'A') | (parts['rule'] == 'R')).all():
        dfs = []
        for _, row in parts.iterrows():
            dfs.append(process_range(row, rules))
        parts = pd.concat(dfs)
    parts = parts[parts.rule == 'A']
    for var in 'xmas':
        parts[var] = parts[var].apply(lambda x: x[1]) - parts[var].apply(lambda x: x[0])
    parts['variants'] = parts.x * parts.m * parts.a * parts.s
    return parts['variants'].sum()


def solve(filename, solve_func):
    with open(f"data/{filename}", 'r') as input_file:
        puzzle_input = [line.replace('\n', '') for line in input_file.readlines()]
    rules = {}
    parts = pd.DataFrame(columns=['x', 'm', 'a', 's'])
    for line in puzzle_input:
        rule_regex = re.compile(r'^(\w+)\{(.+)}$')
        part_regex = re.compile(r'^\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}$')
        rule_match = rule_regex.match(line)
        part_match = part_regex.match(line)
        if rule_match:
            name, steps = rule_match.group(1, 2)
            steps = steps.split(',')
            checks = []
            for step in steps[:-1]:
                condition, next_rule = step.split(':')
                checks.append((condition, next_rule))
            checks.append((None, steps[-1]))
            rules[name] = checks
        if part_match:
            x, m, a, s = map(int, part_match.groups())
            parts.loc[len(parts)] = [x, m, a, s]
    return solve_func(rules, parts)


if __name__ == '__main__':
    print(solve("day19.txt", first))
    print(solve("day19.txt", second))
