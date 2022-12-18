from __future__ import annotations
from functools import cmp_to_key
import re 
import math
import glob
import time
import itertools

FlowRate = int
Pipe = tuple[list[str], FlowRate]

class Frame:

	def __init__(self, pipes, minute) -> None:
		self.minute = minute
		self.pipes = pipes
		self.reachable_pipes = {}
		return

	def time_remaining(self):
		return 30 - self.minute

def calc_next_frame(frame: Frame) -> Frame :

	for (pipe_name, (open_pipes, total_pressure)) in frame.reachable_pipes.items():

		next_frame = Frame(frame.pipes, frame.minute + 1, frame.current_pipe)

		for (next_pipe_name, next_pipe_pressure) in frame.pipes[pipe_name]:

			if next_pipe_pressure * next_frame.time_remaining() > next_frame.best_time_for_pipe(next_pipe_name):
				pass
				

			continue
		continue

	raise


class ConstContext:
	def __init__(self, pipes: dict[str, Pipe]) -> None:
		self.pipes = pipes
		return

	def neighbours(self, initial_pipe_name):
		(reachable_pipe_names, _) = self.pipes[initial_pipe_name]
		for neighbour_pipe_name in reachable_pipe_names:
			yield neighbour_pipe_name
		return

	def nonnull_neighbours_with_distance(self, initial_pipe_name, visited_pipes:set|None=None, distance=0):


		if visited_pipes is None:
			visited_pipes = set([initial_pipe_name])
		elif initial_pipe_name in visited_pipes:
			return
		else:
			visited_pipes.add(initial_pipe_name)
			flow_rate = self.get_flow_rate(initial_pipe_name)
			if flow_rate != 0:
				yield (initial_pipe_name, flow_rate)

		for neighbour in self.neighbours(initial_pipe_name):
			yield from self.nonnull_neighbours_with_distance(neighbour, visited_pipes=visited_pipes, distance=distance+1)
			continue

		return
		# raise # your horns

		
	def get_flow_rate(self, pipe_name):
		(_, flow_rate) = self.pipes[pipe_name]
		return flow_rate

	def calc_distances(self) -> dict[tuple[str, str], int]:
		distances = {}
		for pipe in self.pipes:
			for neigbour in self.neighbours(pipe):
				distances[(pipe, neigbour)] = 1
				continue
			continue
		
		changed = True
		while changed:
			changed = False
			for pipe1 in self.pipes:
				for pipe2 in self.pipes:
					for pipe3 in self.pipes:
						d12 = distances.get((pipe1, pipe2))
						d23 = distances.get((pipe2, pipe3))
						d13 = distances.get((pipe1, pipe3))
						if d12 is not None and d23 is not None:
							if d13 is None or d13 > d12 + d23:
								distances[(pipe1, pipe3)] = d12 + d23
								changed = True

		return distances

	def get_nonnull_nodes(self):
		pipes = []

		for name, (_, rate) in self.pipes.items():
			if rate > 0:
				pipes.append(name)
			continue

		return pipes

class Thread:
	def __init__(self, current_pipe, minute, total_flow_so_far, open_pipes) -> None:
		self.minute = minute
		self.total_flow_so_far = total_flow_so_far
		self.current_pipe = current_pipe
		self.open_pipes = open_pipes
		return
	pass

class Cache:
	def __init__(self) -> None:
		self.best_value_on_pipe_by_minute = {}
		return

	pass

def breadth_first_search_v2(const_context: ConstContext, current_pipe_name):
	first_thread = Thread(current_pipe_name, 1, 0, set())
	threads = [first_thread]

	max_time = 30
	for i in range(1, max_time + 1):
		remaining_time = max_time - i

		new_threads : dict[str, Thread] = {}

		for thread in threads:
			for neighbour in const_context.neighbours(thread.current_pipe):
				other_candidate_thread_on_same_node = new_threads.get(neighbour)
				new_candidate_thread = Thread(neighbour, i + 1, thread.total_flow_so_far, thread.open_pipes)
				if other_candidate_thread_on_same_node is None:
					new_threads[neighbour] = new_candidate_thread
					continue
				if new_candidate_thread.total_flow_so_far > other_candidate_thread_on_same_node.total_flow_so_far:
					new_threads[neighbour] = new_candidate_thread
				continue

			if const_context.get_flow_rate(thread.current_pipe) > 0 and thread.current_pipe not in thread.open_pipes:
				open_pipes = set(thread.open_pipes)
				open_pipes.add(thread.current_pipe)

				other_candidate_thread_on_same_node = new_threads.get(thread.current_pipe)
				new_candidate_thread = Thread(thread.current_pipe, i + 1, thread.total_flow_so_far + remaining_time * const_context.get_flow_rate(thread.current_pipe), open_pipes)

				if other_candidate_thread_on_same_node is None or new_candidate_thread.total_flow_so_far > other_candidate_thread_on_same_node.total_flow_so_far:
					new_threads[thread.current_pipe] = new_candidate_thread
			continue

		threads = list(new_threads.values())

	best_thread = max(threads, key=lambda thread: thread.total_flow_so_far)
	# max_flow = None
	# for thread in threads:
	# 	if max_flow is None:
	# 		max_flow = thread.total_flow_so_far
	# 	else:
	# 		max_flow = max(max_flow, thread.total_flow_so_far)

	print(best_thread.total_flow_so_far)

	return

def breadth_first_search_v3(const_context: ConstContext, current_pipe_name):
	first_thread = Thread(current_pipe_name, 1, 0, set())
	threads = [first_thread]

	finished_threads = []

	max_time = 30
	for _ in range(1, max_time + 1):
		#remaining_time = max_time - i
		new_threads = []
		for thread in threads:
			for (neighbour, distance) in const_context.nonnull_neighbours_with_distance(thread.current_pipe):
				if thread.minute + distance > max_time:
					finished_threads.append(thread)
					continue

				new_candidate_thread = Thread(neighbour, thread.minute + distance, thread.total_flow_so_far, thread.open_pipes)
				new_threads.append(new_candidate_thread)
				
				continue

			if const_context.get_flow_rate(thread.current_pipe) > 0 and thread.current_pipe not in thread.open_pipes:

				if thread.minute + 1 > max_time:
					finished_threads.append(thread)
					continue

				open_pipes = set(thread.open_pipes)
				open_pipes.add(thread.current_pipe)
				remaining_time = max_time - thread.minute

				new_candidate_thread = Thread(thread.current_pipe, thread.minute + 1, thread.total_flow_so_far + remaining_time * const_context.get_flow_rate(thread.current_pipe), open_pipes)
				new_threads.append(new_candidate_thread)

			continue
		threads = new_threads


	best_thread = max(finished_threads, key=lambda thread: thread.total_flow_so_far)
	# max_flow = None
	# for thread in threads:
	# 	if max_flow is None:
	# 		max_flow = thread.total_flow_so_far
	# 	else:
	# 		max_flow = max(max_flow, thread.total_flow_so_far)

	print(best_thread.total_flow_so_far)

	return

def breadth_first_search(const_context: ConstContext, current_pipe_name: str, current_thread: Thread, cache: Cache):



	for neighbour_name in const_context.neighbours(current_pipe_name):
		yield from breadth_first_search(const_context, neighbour_name)


	raise


class Graph:
	def __init__(self, const_context: ConstContext):
		self.const_context = const_context
		self.distances = const_context.calc_distances()
		return



	pass

def graph_solve(const_context: ConstContext):

	starting_pipe = 'AA'
	distances = const_context.calc_distances()
	pipes = const_context.get_nonnull_nodes()


	def calc_released_steam_for_order(pipes: list[str]):
		nonlocal distances
		nonlocal starting_pipe
		nonlocal const_context

		total_released_steam = 0
		remaining_time = 30
		current_pipe = starting_pipe

		for next_pipe in pipes:
			remaining_time -= distances[(current_pipe, next_pipe)] + 1

			flow_rate = const_context.get_flow_rate(next_pipe)
			released_steam = flow_rate * remaining_time
			total_released_steam += released_steam
			current_pipe = next_pipe

		return total_released_steam

	
	max = None
	for pipe_order in itertools.permutations(pipes):
		released_steam = calc_released_steam_for_order(pipe_order) 
		if max is None or released_steam > max:
			max = released_steam


	print(max)
	return


def solve(lines):
	# Valve AA has flow rate=0; tunnels lead to valves DD, II, BB

	pipes : list[Pipe] = {}

	for line in lines:
		(this_pipe_name, str_flow_rate, str_list_of_access) = re.match(r'^Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.*)$', line).groups()
		flow_rate = int(str_flow_rate)

		dest_pipe_names: list[str] = []
		for pipe_to_name in re.findall(r'(\w+)', str_list_of_access):
			dest_pipe_names.append(pipe_to_name)
			continue

		pipes[this_pipe_name] = (dest_pipe_names, flow_rate)

	const_context = ConstContext(pipes)

	starting_pipe = 'AA'

	#breadth_first_search_v2(const_context, starting_pipe)
	#breadth_first_search_v3(const_context, starting_pipe)
	graph_solve(const_context)

	# frame = Frame(pipes, 1)
	# frame.reachable_pipes = {starting_pipe: ([], 0)}

	# calc_next_frame(frame)


	return





for filename in glob.glob("inputs/*.txt"):
	with open(filename) as file:
		lines = list(map(lambda s: str.strip(s, "\n"), file.readlines()))
	print(filename)
	start = time.time()

	solve(lines)
	
	end = time.time()
	print(f'Solve time: {end - start}')
	print("------------------")



