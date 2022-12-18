from __future__ import annotations
from functools import cmp_to_key
import re 
import math
import glob

def calc_distance(a, b):
	return abs(b[0] - a[0]) + abs(b[1] - a[1])

def solve(lines):

	sensor_beacon_pairs = []

	queried_row_y = None
	for line in lines:
		if result := re.match(r'y=(\d+)', line):
			queried_row_y = int(result.group(1))
		if result := re.match(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)', line):
			sensor_pos = (int(result.group(1)), int(result.group(2)))
			beacon_pos = (int(result.group(3)), int(result.group(4)))
			sensor_beacon_pairs.append((sensor_pos, beacon_pos))

	assert(queried_row_y is not None)

	intervals = []
	events = []

	kIntervalStart = 1
	kIntervalEnd = 2

	for (sensor_pos, beacon_pos) in sensor_beacon_pairs:
		radius = calc_distance(sensor_pos, beacon_pos)
		distance_from_row = abs(queried_row_y - sensor_pos[1])
		if distance_from_row < radius:
			interval_range = radius - distance_from_row
			interval = (sensor_pos[0] - interval_range, sensor_pos[0] + interval_range)
			intervals.append(interval)
			events.append((kIntervalStart, interval[0]))
			events.append((kIntervalEnd, interval[1]))
		continue

	
	events = sorted(events, key=lambda e: e[1])

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
				pass
			pass
		else:
			assert()
		continue

	print(sum)





for filename in glob.glob("inputs/*.txt"):
	with open(filename) as file:
		lines = list(map(lambda s: str.strip(s, "\n"), file.readlines()))
	print(filename)
	solve(lines)
	print("------------------")


