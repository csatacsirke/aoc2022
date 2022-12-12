from operator import contains
import re

def parse_line_stage_0(line, crate_columns: dict[int, str]):
	#[R] [J] [S] [Z] [R] [S] [D] [L] [J]
	for i in range(0, len(line)):
		if i % 4 != 1:
			continue
		if line[i] == " ":
			continue
		column_index = i // 4 + 1
		
		list_of_crates = crate_columns.get(column_index, [])
		list_of_crates.insert(0, line[i])
		crate_columns[column_index] = list_of_crates
		
	return

def parse_line_stage2_an_do_operation(line, crate_columns: dict[int, list[str]]):
	#move 1 from 2 to 1
	matches = re.match(r'move (\d+) from (\d+) to (\d+)', line)
	(n, index_from, index_to) = list(map(int, matches.groups()))

	column_from = crate_columns.get(index_from)
	column_to = crate_columns.get(index_to)
	#for _ in range(0, n):
	#    column_to.append(column_from.pop())
	
	temp_list = []
	for _ in range(0, n):
		temp_list.append(column_from.pop())

	for _ in range(0, n):
		column_to.append(temp_list.pop())

	return 

def solve(lines):

	crate_columns = {}
	file_stage = 0
	for line in lines:
		if file_stage == 0:
			if line[1] == '1':
				file_stage = 1
				continue
			
			parse_line_stage_0(line, crate_columns) 
			pass
		if file_stage == 1:
			file_stage = 2
			continue
		if file_stage == 2:
			parse_line_stage2_an_do_operation(line, crate_columns)

	print()
	for i in range(1, 10):
		val = crate_columns.get(i)
		if val is None:
			break

		print(val[-1], end="")
	print()
	return

files = ["example.txt", "input.txt"]

for filename in files:
	with open(filename) as file:
		lines = list(map(lambda s: str.strip(s, "\n"), file.readlines()))
	print(filename)
	solve(lines)
	print("------------------")





