
def solve_line(line):

	for i in range(0, len(line)):
		if len(set(line[i:i+14])) == 14:
			return i + 14

	raise

def solve(lines):
	for line in lines:
		print(solve_line(line))
	

files = ["example.txt", "input.txt"]

for filename in files:
	with open(filename) as file:
		lines = list(map(lambda s: str.strip(s, "\n"), file.readlines()))
	print(filename)
	solve(lines)
	print("------------------")





