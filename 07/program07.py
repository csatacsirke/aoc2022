from __future__ import annotations
import re 

def solve_line(line):

	for i in range(0, len(line)):
		if len(set(line[i:i+14])) == 14:
			return i + 14

	raise

class File:
	def __init__(self, size: int):
		self.size = size

class Dir:
	def __init__(self, parent = None):
		self.parent: Dir = parent
		self.child_dirs: dict[str, Dir] = {}
		self.files: dict[str, File] = {}
		self.size: int = 0

	def get_child_dir(self, name):
		if dir := self.child_dirs.get(name):
			return dir
		new_dir = Dir(parent=self)

		a1 = id(new_dir.child_dirs)
		a2 = id(self.child_dirs)

		self.child_dirs[name] = new_dir
		
		assert(new_dir is not self)

		return new_dir

	def add_file(self, file_name, file_size):
		#assert( self.files.get(file_name) == None)
		if self.files.get(file_name) != None:
			# vótmá
			#(As in this example, this process can count files more than once!) ???
			return

		self.files[file_name] = File(file_size)

		self.update_size(file_size)

	def update_size(self, file_size):
		self.size = self.size + file_size
		if self.parent != None:
			self.parent.update_size(file_size)

class Shell:
	def __init__(self) -> None:
		self.root = Dir()
		self.current_dir = self.root
		pass
	

def process_line(shell: Shell, line: str):
	if line == "$ ls":
		return

	if line == "$ cd /":
		shell.current_dir = shell.root
		return

	if line == "$ cd ..":
		shell.current_dir = shell.current_dir.parent
		return

	if match_result := re.match(r'\$ cd (.*)', line):
		(dir_name,) = match_result.groups()
		child_dir = shell.current_dir.get_child_dir(dir_name)
		shell.current_dir = child_dir
		return 
	if match_result := re.match(r'dir (.*)', line):
		#dir e
		return
	if match_result := re.match(r'(\d+) (.*)', line):
		#29116 f
		file_size = int(match_result.group(1))
		file_name = match_result.group(2)
		shell.current_dir.add_file(file_name, file_size)
		return
	raise

def traverse_dirs(dir: Dir, fn):

	fn(dir)

	for _, child_dir in dir.child_dirs.items():
		traverse_dirs(child_dir, fn)


def pretty_print(dir: Dir, level = 0):
	
	for (name, child_dir) in dir.child_dirs.items():
		for _ in range(0, level):
			print(' ', end='')

		print(f'{name} - DIR size: {child_dir.size}')
		pretty_print(child_dir, level + 1)

	for (name, file) in dir.files.items():
		#break
		for _ in range(0, level):
			print(' ', end='')
		print(f'{name} - size: {file.size}')

	return

def solve(lines):
	shell = Shell()

	for line in lines:
		process_line(shell, line)

	total = 0
	def process_dir(dir: Dir):
		if dir.size <= 100000:
			nonlocal total
			total += dir.size
		return

	#pretty_print(shell.root)
	if False:
		traverse_dirs(shell.root, process_dir)
		print(total)


	disk_size = 70000000
	required_size = 30000000
	available_size = disk_size - shell.root.size
	need_to_free_at_least = required_size - available_size

	min = None
	def process_dir2(dir: Dir):
		nonlocal min
		if dir.size < need_to_free_at_least:
			return
		if min is None or min > dir.size:
			min = dir.size
		
		return

	traverse_dirs(shell.root, process_dir2)
	print(min)
	

files = ["example.txt", "input.txt"]

for filename in files:
	with open(filename) as file:
		lines = list(map(lambda s: str.strip(s, "\n"), file.readlines()))
	print(filename)
	solve(lines)
	print("------------------")





class MyClass:
	my_dict = {}




