from __future__ import annotations
import re 

width = 0
height = 0

def calc_view_index(grid: dict[tuple[int, int], tuple[int, bool]], x: int, y: int):
	(this_tree_height, is_visible) = grid[(x, y)]
	
	view_index = 1

	i = x
	for i in range(x+1, width):
		(other_tree_height, _) = grid[(i, y)]
		if other_tree_height >= this_tree_height or i == width -1:
			break
	view_index *= abs(i - x)

	i = x
	for i in range(x-1, -1, -1):
		(other_tree_height, _) = grid[(i, y)]
		if other_tree_height >= this_tree_height or i == 0:
			break
	view_index *= abs(i - x)

	i = y
	for i in range(y+1, height):
		(other_tree_height, _) = grid[(x, i)]
		if other_tree_height >= this_tree_height or i == height -1 :
			break

	view_index *= abs(i - y)
	i = y
	for i in range(y-1, -1, -1):
		(other_tree_height, _) = grid[(x, i)]
		if other_tree_height >= this_tree_height or i == 0:
			break
	view_index *= abs(i - y)

	return view_index

def solve(lines):

	grid = {}

	global width 
	global height


	y = 0
	for line in lines:
		x = 0
		for char in line:
			grid[(x, y)] = (int(char), False)
			x += 1
			width = max(width, x)
		y += 1
		height = max(height, y)
	
	for x in range(0, width):
		max_height = -1
		for y in range(0, height):

			(tree_height, _) = grid[(x, y)]
			if tree_height > max_height:
				grid[(x, y)] = (tree_height, True)
			max_height = max(max_height, tree_height)
			continue
		continue

	for x in range(0, width):
		max_height = -1
		for y in range(height - 1, 0, -1):
			(tree_height, _) = grid[(x, y)]
			if tree_height > max_height:
				grid[(x, y)] = (tree_height, True)
			max_height = max(max_height, tree_height)
			continue
		continue

	for y in range(0, height):
		max_height = -1
		for x in range(0, width):
			(tree_height, _) = grid[(x, y)]
			if tree_height > max_height:
				grid[(x, y)] = (tree_height, True)
			max_height = max(max_height, tree_height)
			continue
		continue

	for y in range(0, height):
		max_height = -1
		for x in range(width-1, 0, -1):
			(tree_height, _) = grid[(x, y)]
			if tree_height > max_height:
				grid[(x, y)] = (tree_height, True)
			max_height = max(max_height, tree_height)
			continue
		continue

	visible_count = 0
	for i in range(0, height):
		for j in range(0, width):
			(tree_height, is_visible) = grid[(i, j)]
			if is_visible:
				visible_count += 1


	#print(visible_count)

	best_view_index = None
	for i in range(0, height):
		for j in range(0, width):
			view_index = calc_view_index(grid, i, j)
			if best_view_index is None or best_view_index < view_index:
				best_view_index = view_index

	print(best_view_index)
	return
	

files = ["example.txt", "input.txt"]

for filename in files:
	with open(filename) as file:
		lines = list(map(lambda s: str.strip(s, "\n"), file.readlines()))
	print(filename)
	solve(lines)
	print("------------------")





class MyClass:
	my_dict = {}




