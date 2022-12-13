from __future__ import annotations
import re 
import math


def is_right_order(packet1, packet2):
	

	if type(packet1) is int and type(packet2) is int:
		if packet1 < packet2:
			return True
		if packet1 > packet2:
			return False
		return None
	
	if type(packet1) is list and type(packet2) is list:
		for i in range(0, min(len(packet1), len(packet2))):
			result = is_right_order(packet1[i], packet2[i])
			if result is not None:
				return result 
			
			continue
		if len(packet1) == len(packet2):
			return None
		
		return len(packet1) < len(packet2)

	if type(packet1) is int:
		assert(type(packet2) is list)
		return is_right_order([packet1], packet2)

	if type(packet2) is int:
		assert(type(packet1) is list)
		return is_right_order(packet1, [packet2])

	raise


def solve(lines):

	iterator = iter(lines)

	pairs = []

	while line1 := next(iterator, None):
		line2 = next(iterator)
		_ = next(iterator, None)

		packet1 = eval(line1)
		packet2 = eval(line2)
		pairs.append((packet1, packet2))

	final_result = 0
	for i in range(0, len(pairs)):
		result = is_right_order(*pairs[i])
		assert(result is not None)
		if result:
			final_result += (i + 1)
		
		continue

	print(final_result)

	return 



files = ["example.txt", "input.txt"]

for filename in files:
	with open(filename) as file:
		lines = list(map(lambda s: str.strip(s, "\n"), file.readlines()))
	print(filename)
	solve(lines)
	print("------------------")


