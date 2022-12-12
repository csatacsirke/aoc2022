
def find_priority(char):
    
    if ord(char) >= ord('a') and ord(char) <= ord('z'):
        return ord(char) - ord('a') + 1

    if ord(char) >= ord('A') and ord(char) <= ord('Z'):
        return ord(char) - ord('A') + 27
    raise


def find_conflicting(rucksack: tuple[str, str]):
    (a, b) = rucksack

    chars_a = set(a)
    chars_b = set(b)

    intersection = set.intersection(chars_a, chars_b)
    assert(len(intersection) == 1)
    return intersection.pop()



def solve1(lines):
    rucksacks = list(map(lambda x: (x[0:len(x)//2], x[len(x)//2:]), lines))
    conflicts = list(map(find_conflicting, rucksacks))
    priorities = list(map(find_priority, conflicts))
    total = sum(priorities)
    print(total)
    pass


def find_badge(group: tuple[str, str, str]):
    chars = set(group[0])
    chars = chars.intersection(group[1])
    chars = chars.intersection(group[2])
    assert(len(chars) == 1)
    return chars.pop()

def solve(lines):

    groups = []
    for i in range(0, len(lines)//3):
        group = (lines[3*i], lines[3*i+1], lines[3*i+2])
        groups.append(group)
    
    badges = list(map(find_badge, groups))
    priorities = list(map(find_priority, badges))
    total = sum(priorities)
    print(total)



files = ["example.txt", "input.txt"]

for filename in files:
    with open(filename) as file:
        lines = list(map(str.strip, file.readlines()))
    print(filename)
    solve(lines)
    print("------------------")





