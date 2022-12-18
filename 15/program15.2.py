from __future__ import annotations
from functools import cmp_to_key
import re 
import math
import glob
import time

def calc_distance(a, b):
	return abs(b[0] - a[0]) + abs(b[1] - a[1])

def return_x_if_row_has_empty_position(sensor_beacon_pairs, search_space_size, queried_row_y):

	def normalize(x):
		nonlocal search_space_size
		x = min(x, search_space_size)
		x = max(x, 0)
		return x
	#intervals = []
	events = []

	kIntervalStart = 1
	kIntervalEnd = 2

	for (sensor_pos, beacon_pos) in sensor_beacon_pairs:
		radius = calc_distance(sensor_pos, beacon_pos)
		distance_from_row = abs(queried_row_y - sensor_pos[1])
		if distance_from_row < radius:
			interval_range = radius - distance_from_row
			interval = (sensor_pos[0] - interval_range, sensor_pos[0] + interval_range)
			#intervals.append(interval)
			events.append((kIntervalStart, normalize(interval[0])))
			events.append((kIntervalEnd, normalize(interval[1])))
		continue

	
	#events = sorted(events, key=lambda e: e[1])
	def event_cmp(a, b):
		if a[1] == b[1]:
			if a[0] < b[0]:
				return -1
			if a[0] > b[0]:
				return 1
			return 0
		if a[1] < b[1]:
				return -1
		if a[1] > b[1]:
			return 1
		return 0

	events = sorted(events, key=cmp_to_key(event_cmp))

	the_x = None
	sum = 0
	interval_count = 0
	interval_begin_x = None
	for (event_type, x) in events:
		if event_type == kIntervalStart:
			if interval_count == 0:
				interval_begin_x = x
			interval_count += 1
			pass
		elif event_type == kIntervalEnd:
			interval_count -= 1
			assert(interval_count >= 0)
			if interval_count == 0:
				sum += x - interval_begin_x
				interval_begin_x = None
				if x != search_space_size:
					# there should be only one
					assert(the_x is None)
					the_x = x + 1
				pass
			pass
		else:
			assert()
		continue
	#assert(the_x is not None)
	return the_x
	
def solve(lines):

	sensor_beacon_pairs = []

	search_space_size = None
	for line in lines:
		if result := re.match(r'y=(\d+)', line):
			search_space_size = int(result.group(1))
		if result := re.match(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)', line):
			sensor_pos = (int(result.group(1)), int(result.group(2)))
			beacon_pos = (int(result.group(3)), int(result.group(4)))
			sensor_beacon_pairs.append((sensor_pos, beacon_pos))

	assert(search_space_size is not None)

	for y in range(0, search_space_size+1):
		x = return_x_if_row_has_empty_position(sensor_beacon_pairs, search_space_size, y)
		if x is not None:
			print(x * 4000000 + y)
			return
	raise





for filename in glob.glob("inputs/*.txt"):
	with open(filename) as file:
		lines = list(map(lambda s: str.strip(s, "\n"), file.readlines()))
	print(filename)
	start = time.time()

	solve(lines)
	
	end = time.time()
	print(f'Solve time: {end - start}')
	print("------------------")


