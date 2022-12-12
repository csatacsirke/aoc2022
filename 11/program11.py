from __future__ import annotations
import re 
import math


def make_add(N):
	return lambda x: x + N

def make_square():
	return lambda x: x * x

def make_mul(N):
	return lambda x: x * N

class Monkey:
	def __init__(self, starting_items, operation, divisible_by, monkey_id_if_true, monkey_id_if_false) -> None:
		self.items = starting_items
		self.operation = operation
		self.divisible_by = divisible_by
		self.monkey_id_if_true = monkey_id_if_true
		self.monkey_id_if_false = monkey_id_if_false
		return

	pass

def read_monkies(lines):
	"""
	Monkey 0:
		Starting items: 79, 98
		Operation: new = old * 19
		Test: divisible by 23
			If true: throw to monkey 2
			If false: throw to monkey 3
	"""

	it = iter(lines)
	while True:
		line = next(it, None)
		if line is None:
			break
		if not str.startswith(line, "Monkey"):
			continue

		starting_items_line = next(it)
		operation_line = next(it)
		test_line = next(it)
		true_line = next(it)
		false_line = next(it)

		starting_items = list(map(int, re.findall(r'\d+', starting_items_line)))

		operation = None
		if match := re.match(r'.*new = old \+ (\d+)', operation_line):
			operation = make_add(int(match.group(1)))
		elif match := re.match(r'.*new = old \* (\d+)', operation_line):
			operation = make_mul(int(match.group(1)))
		elif match := re.match(r'.*new = old \* old', operation_line):
			operation = make_square()
		else:
			assert(False)

		divisible_by = int(re.match(r'.*Test: divisible by (\d+)', test_line).group(1))
		monkey_id_if_true = int(re.match(r'.*If true: throw to monkey (\d+)', true_line).group(1))
		monkey_id_if_false = int(re.match(r'.*If false: throw to monkey (\d+)', false_line).group(1))

		yield Monkey(starting_items, operation, divisible_by, monkey_id_if_true, monkey_id_if_false)
		continue
	

	return

def solve(lines):



	monkies = list(read_monkies(lines))

	inspect_count = {}

	for _ in range(0, 20):
		for monkey_index in range(0, len(monkies)):
			monkey = monkies[monkey_index]

			while len(monkey.items) > 0:
				inspect_count[monkey_index] = inspect_count.get(monkey_index, 0) + 1

				item = monkey.items.pop(0)
				item = monkey.operation(item)
				item = item // 3
				if item % monkey.divisible_by == 0:
					monkies[monkey.monkey_id_if_true].items.append(item)
				else:
					monkies[monkey.monkey_id_if_false].items.append(item)
			for item in monkey.items:
				continue

			continue
		continue

	
	print(inspect_count.items())
	print(math.prod(sorted(inspect_count.values())[-2:]))

	return




files = ["example.txt", "input.txt"]

for filename in files:
	with open(filename) as file:
		lines = list(map(lambda s: str.strip(s, "\n"), file.readlines()))
	print(filename)
	solve(lines)
	print("------------------")


