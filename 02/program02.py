from operator import contains

bravery_mapping = {
    'A': 1,
    'B': 2,
    'C': 3,
}

def decrypt(xyz):
    mapping = {
        'X': 'A',
        'Y': 'B',
        'Z': 'C',
    }
    return mapping[xyz]

def calc_winner_score(opponent, ours):
    if opponent == ours:
        return 3
    
    winning_mapping = {
        'A': 'C',
        'B': 'A',
        'C': 'B',
    }
    if winning_mapping[ours] == opponent:
        return 6

    return 0

def get_required(opponent, desired_result):

    winning_mapping = {
        'A': 'C',
        'B': 'A',
        'C': 'B',
    }
    draw_mapping = {
        'A': 'A',
        'B': 'B',
        'C': 'C',
    }
    losing_mapping = {
        'A': 'B',
        'B': 'C',
        'C': 'A',
    }
    if desired_result == 'Z':
        mapping = losing_mapping
    
    if desired_result == 'Y':
        mapping = draw_mapping

    if desired_result == 'X':
        mapping = winning_mapping

    return mapping[opponent]


def calc_match_score(match):
    opponent = match[0] 
    #ours = decrypt(match[1]) 
    ours = get_required(opponent, match[1])
    score_part_1 = calc_winner_score(opponent, ours)
    score_part_2 = bravery_mapping[ours]
    score = score_part_1 + score_part_2
    print(score, end=' ')
    return score 

def solve(lines):
    
    matches = map(lambda x: x.split(' '), lines)
    total = sum(map(calc_match_score, matches))
    print(total)
    pass


files = ["example.txt", "input.txt"]

for filename in files:
    with open(filename) as file:
        lines = list(map(str.strip, file.readlines()))
    print(filename)
    solve(lines)
    print("------------------")





