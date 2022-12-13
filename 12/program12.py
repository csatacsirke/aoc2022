from __future__ import annotations
import re 
import math
#from typing import Dict, Tuple

Point = tuple[int, int]
HeightMap = dict[Point, int]
#DoneList = list[tuple[Point, Point, int]]
DoneMap = dict[Point, tuple[Point, int]]
OpenList = list[tuple[Point, Point, int]]

def letter_to_height(letter):
	if ord(letter) >= ord('a') and ord(letter) <= ord('z'):
		return ord(letter) - ord('a')

	if letter == 'S':
		return letter_to_height('a')
	
	if letter == 'E':
		return letter_to_height('z')

	raise

def parse_lines(lines):
	height_map: HeightMap = {}

	start = None
	end = None

	for y in range(0, len(lines)):
		line = lines[y]
		for x in range(0, len(line)):
			letter = line[x]
			height_map[(x, y)] = letter_to_height(letter)
			
			if letter == 'S':
				start = (x,y)
			
			if letter == 'E':
				end = (x,y)

			continue
		continue

	assert(start is not None)
	assert(end is not None)

	return (height_map, start, end)

def reachable_neighbours(height_map: dict, p, inverse = False):
	(x, y) = p

	neighbours = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
	for neighbour in neighbours:
		if height_map.get(neighbour) is not None:
			if inverse:
				if climbing_is_possible(height_map, neighbour, p):
					yield neighbour
			else:
				if climbing_is_possible(height_map, p, neighbour):
					yield neighbour

	return 

def open_list_contains(open_list: OpenList, point: Point):
	for (p, _, _) in open_list:
		if p == point:
			return True
	return False

def climbing_is_possible(height_map: HeightMap, from_point: Point, to_point: Point):

	height_from = height_map.get(from_point)
	height_to = height_map.get(to_point)
	assert(height_from is not None)
	assert(height_to is not None)

	if height_to - height_from <= 1:
		return True
	return False

def iterate_pathfinding(height_map: HeightMap, open: OpenList, done: DoneMap):
	while len(open) > 0:
		(current_point, from_point, distance_from_start) = open.pop(0)

		for neighbour_point in reachable_neighbours(height_map, current_point):
			if neighbour_point not in done and not open_list_contains(open, neighbour_point): #and climbing_is_possible(height_map, current_point, neighbour_point):
				open.append((neighbour_point, current_point, distance_from_start + 1))
			continue

		for neighbour_point in reachable_neighbours(height_map, current_point, inverse=True):
			if value := done.get(neighbour_point):
				(_, neighbour_distance_from_start) = value
				if neighbour_distance_from_start + 1 < distance_from_start:
					distance_from_start = neighbour_distance_from_start + 1
					from_point = neighbour_point
			continue

		done[current_point] = (from_point, distance_from_start)

	return

def debug_print_done_map2(done_map: DoneMap):
	max_x = 0
	max_y = 0
	for (x, y) in done_map.keys():
		max_x = max(max_x, x)
		max_y = max(max_y, y)
		
	for y in range(0, max_y):
		for x in range(0, max_x):
			opt_entry = done_map.get((x, y))
			if opt_entry is None:
				print('.', end='')
			else:
				((from_x, from_y), _) = opt_entry
				char = 'S'
				if from_x - x < 0:
					char = '>'
				if from_x - x > 0:
					char = '<'
				if from_y - y < 0:
					char = 'v'
				if from_y - y > 0:
					char = '^'

				print(char, end='')
			continue
		print()
		continue
	print()
	return

def debug_print_done_map(done_map: DoneMap):
	
	visual_map = {}

	for ((x, y), ((from_x, from_y), _)) in done_map.items():
		char = '?'
		if from_x - x < 0:
			char = '>'
		if from_x - x > 0:
			char = '<'
		if from_y - y < 0:
			char = 'v'
		if from_y - y > 0:
			char = '^'

		visual_map[(from_x, from_y)] = char
		continue

	max_x = 0
	max_y = 0
	for (x, y) in visual_map.keys():
		max_x = max(max_x, x)
		max_y = max(max_y, y)
		
	for y in range(0, max_y):
		for x in range(0, max_x):
			opt_char = visual_map.get((x, y))
			if opt_char is None:
				print('.', end='')
			else:
				print(opt_char, end='')
			continue
		print()
		continue

	print()
	return

def solve_trial(height_map, start, end):
	
	open: OpenList = [ (start, start, 0) ]
	done_map: DoneMap = {}

	iterate_pathfinding(height_map, open, done_map)

	#debug_print_done_map(done_map)

	result = done_map.get(end)
	if result is None:
		return None
	
	(point_from, distance_from_start) = result
	return distance_from_start
	
def solve(lines):

	(height_map, _, end) = parse_lines(lines)
	
	min_result = 100000
	for (point, height) in height_map.items():
		if height == 0:
			result = solve_trial(height_map, point, end)
			if result is None:
				continue
			min_result = min(min_result, result)


	print(min_result)

	return




files = ["example.txt", "input.txt"]

for filename in files:
	with open(filename) as file:
		lines = list(map(lambda s: str.strip(s, "\n"), file.readlines()))
	print(filename)
	solve(lines)
	print("------------------")


