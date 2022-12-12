import re

def parse_line(line: str):
    matches = re.match(r'(\d+)-(\d+),(\d+)-(\d+)', line)
    
    return list(map(int, matches.groups()))

def fully_contains(group):
    if group[0] >= group[3] and group[1] <= group[3]:
        return 1
    
    if group[0] <= group[2] and group[1] >= group[3]:
        return 1

    return 0

def range_includes(a, b, x):
    return a <= x and x <= b

def overlaps(group):

    if range_includes(group[2], group[3], group[0]):
        return True
    if range_includes(group[2], group[3], group[1]):
        return True

    if range_includes(group[0], group[1], group[2]):
        return True
    if range_includes(group[0], group[1], group[3]):
        return True

    return False


def solve(lines):
    groups = list(map(parse_line, lines))
    total = sum(list(map(overlaps, groups)))
    print(total)

def solve1(lines):
    groups = list(map(parse_line, lines))
    total = sum(list(map(fully_contains, groups)))
    print(total)

files = ["example.txt", "input.txt"]

for filename in files:
    with open(filename) as file:
        lines = list(map(str.strip, file.readlines()))
    print(filename)
    solve(lines)
    print("------------------")





