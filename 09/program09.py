from __future__ import annotations
import re 
import operator

def parse_line(line):
	(dir, N) = re.match(r'(\w) (\d+)', line).groups()
	N = int(N)

	delta = (0, 0)
	if dir == 'D':
		delta = (0, -1)

	if dir == 'U':
		delta = (0, 1)

	if dir == 'L':
		delta = (-1, 0)

	if dir == 'R':
		delta = (1, 0)


	return [delta] * N
def sign(x):
	if x == 0:
		return 0
	if x < 0:
		return -1
	if x > 0:
		return 1
	raise

def solve(lines):
	# head = (0, 0)
	# tail = (0, 0)
	knots = [(0, 0)] * 10

	visited_positions = set()

	for line in lines:
		deltas = parse_line(line)
		for delta in deltas:
			
			knots[0] = tuple(map(operator.add, knots[0], delta))

			for i in range(0, len(knots) - 1):
				head = knots[i]
				tail = knots[i + 1]

				head_tail_delta = tuple(map(operator.sub, head, tail))


				tail_compensation = (0, 0)
				if abs(head_tail_delta[0]) * abs(head_tail_delta[1]) == 0 and abs(head_tail_delta[0]) + abs(head_tail_delta[1]) == 1:
					pass
				elif abs(head_tail_delta[0]) * abs(head_tail_delta[1]) == 1 and abs(head_tail_delta[0]) + abs(head_tail_delta[1]) == 2:
					pass
				else:
					tail_compensation = (sign(head_tail_delta[0]), sign(head_tail_delta[1]))
				

				assert(abs(tail_compensation[0]) + abs(tail_compensation[1]) <= 2)
				
				tail = tuple(map(operator.add, tail, tail_compensation))
				
				knots[i] = head
				knots[i+1] = tail

				continue
			visited_positions.add(knots[9])
			continue

		continue

	print(len(visited_positions))
	return
	

files = ["example.txt", "example2.txt", "input.txt"]

for filename in files:
	with open(filename) as file:
		lines = list(map(lambda s: str.strip(s, "\n"), file.readlines()))
	print(filename)
	solve(lines)
	print("------------------")




