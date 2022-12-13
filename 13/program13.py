from __future__ import annotations
from functools import cmp_to_key
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

def cmp_right_order(a, b):
	result = is_right_order(a, b)
	if result is None:
		return 0
	if result is True:
		return -1
	return 1

def solve(lines):

	iterator = iter(lines)

	pairs = []

	packets = []

	while line1 := next(iterator, None):
		line2 = next(iterator)
		_ = next(iterator, None)

		packet1 = eval(line1)
		packet2 = eval(line2)
		
		packets.append(packet1)
		packets.append(packet2)

		pairs.append((packet1, packet2))

	final_result = 0
	for i in range(0, len(pairs)):
		result = is_right_order(*pairs[i])
		assert(result is not None)
		if result:
			final_result += (i + 1)
		
		continue

	divider1 = [[2]]
	divider2 = [[6]]

	packets.append(divider1)
	packets.append(divider2)

	#print(final_result)
	sorted_packets = sorted(packets, key=cmp_to_key(cmp_right_order))
	#packets.sort(key=cmp_right_order)
	
	divider1_index = None
	divider2_index = None

	for i in range(0, len(sorted_packets)):
		if cmp_right_order(sorted_packets[i], divider1) == 0:
			divider1_index = i + 1
		if cmp_right_order(sorted_packets[i], divider2) == 0:
			divider2_index = i + 1


	print(divider1_index * divider2_index)


	return 



files = ["example.txt", "input.txt"]

for filename in files:
	with open(filename) as file:
		lines = list(map(lambda s: str.strip(s, "\n"), file.readlines()))
	print(filename)
	solve(lines)
	print("------------------")


