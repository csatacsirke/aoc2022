from __future__ import annotations
import re 


class AddOperation:
	def __init__(self, N) -> None:
		self.N = N
		return

	def cycle(self, cpu: CPU):
		yield
		yield
		cpu.sprite_position += self.N
		return
	pass

class NoOperation:
	def cycle(self, cpu: CPU):
		yield
		return
	pass

class CPU:



	def __init__(self):
		self.sprite_position = 1
		self.sum = 0
		self.cycle_index = 1
		self.pixels = [0] * 240
		return

	def run_operation(self, operation):
		for _ in operation.cycle(self):
			self.on_cycle()
			continue

		return

	def on_cycle(self):
		# 20th, 60th, 100th, 140th, 180th, and 220th
		if self.cycle_index in [20, 60, 100, 140, 180, 220]:
			self.sum += self.sprite_position * self.cycle_index

		if abs(self.sprite_position - self.cycle_index % 40 + 1) <= 1:
			self.pixels[self.cycle_index] = 1
		
		self.cycle_index += 1
		return
	pass


def print_crt_pixels(pixels: list[int]):
	# 40x6

	for i in range(0, len(pixels)):
		print(' ' if pixels[i] == 0 else 'X', end="")
		if i % 40 == 0:
			print()
			pass
	print()
	return

def solve(lines):
	cpu = CPU()

	for line in lines:
		# addx -21
		if match := re.match(r'addx (-?\d+)', line):
			value = int(match.group(1))
			cpu.run_operation(AddOperation(value))
		if line == 'noop':
			cpu.run_operation(NoOperation())

	print(cpu.sum)
	print_crt_pixels(cpu.pixels)
	#raise




files = ["example.txt", "input.txt"]

for filename in files:
	with open(filename) as file:
		lines = list(map(lambda s: str.strip(s, "\n"), file.readlines()))
	print(filename)
	solve(lines)
	print("------------------")


