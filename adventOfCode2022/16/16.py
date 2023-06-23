# Loading relevant libraries
import re 
from itertools import combinations
from collections import defaultdict, deque

def main():	
	# Closest paths 
	paths = {}
	
	# Part 1
	if False:
		# List of valves and their connections/fr + state of system
		valves, state = process_data()
		state["t"] = 30
		state["source"] = "AA"
		state["pr"] = 0 # Pressure relief
		
		# Finding all possible points
		mo = [0]
		point_search(valves, paths, state, mo = mo)
		print(mo)
	
	# Part 2
	# List of valves and their connections/fr + state of system
	valves, state = process_data()
	state["t"] = 26
	state["pr"] = 0 # Pressure relief
	state["source"] = "AA"
	
	# Finding all possible points
	MO = double_search(valves, paths, state)
	print(MO)
	
def double_search(valves: dict, paths: dict, state: dict) -> int:
	MT = 0
	n = len([v for v in valves if valves[v]["F"]])//2 # Number of valves per combination
	for c0 in combinations([v for v in valves if valves[v]["F"]], n):
		c1 = tuple(v for v in valves if not v in c0)
		MO0 = [0]
		MO1 = [0]
		# Getting the maximum score for mO0
		# Only open valves that exist in c0
		to_remove = []
		for v in c1:
			if not v in state["open"]:
				state["open"].append(v)
				to_remove.append(v)
		# Run maximization on v0
		point_search(valves, paths, state, MO0)
		
		# Getting maximum score for mo1
		# Only open valves that exist in c1
		while to_remove:
			state["open"].remove(to_remove.pop())
		for v in c0:
			if not v in state["open"]:
				state["open"].append(v)
				to_remove.append(v)
		# Running maximization for v1
		point_search(valves, paths, state, MO1)
		# Removing unwanted open valves
		while to_remove:
			state["open"].remove(to_remove.pop())
			
		MT = max(MT, MO0[0]+MO1[0])
	return MT
		
	
def point_search(valves: dict, paths: dict, state: dict, mo: iter):
		
	# If current highest value is higher than maximum value, stop this branch
	closed_valves = tuple(v for v in valves if not v in state["open"]) 
	if mo[0] > calc_max_possible(valves, state, closed_valves):
		pass
	
	# Checking if current iteration is highest
	mo[0] = max(mo[0], state["pr"])
		
	# Checking rest of branch
	source = state["source"]
	for target in closed_valves:		
		# Moving and chosing a new path
		path = get_closest_path(paths, valves, source, target)
		dt = len(path) + 1 # 1 comes from turning on the tap
		
		# Removing transportation time + opening valve
		if state["t"]-dt > 0:
			state["t"] -= dt
			state["open"].append(target)
			points = valves[target]["F"]*state["t"]
			state["pr"] += points
			state["source"] = target
			point_search(valves, paths, state, mo)
			state["source"] = source
			state["pr"] -= points
			state["open"].remove(target)
			state["t"] += dt
			
		
		
def calc_max_possible(valves: dict, state: dict, closed_valves: iter) -> int:
	remaining = sum(valves[cv]["F"]*(state["t"]-2) for cv in closed_valves) if closed_valves and state["t"] > 1 else 0
	return remaining + state["pr"]
	
def dijkstra(valves: dict, source: str) -> iter:
	dist = {v: 1e6 for v in valves}
	prev = {v: None for v in valves}
	Q = set(valves)
	dist[source] = 0
	while Q:
		u = min(Q, key = lambda U: dist[U])
		Q.remove(u)
		
		for neighbour in valves[u]["out"]:
			alt = dist[u] + 1
			if alt < dist[neighbour]:
				dist[neighbour] = alt
				prev[neighbour] = u
				
	return dist, prev
	
def dijkstra_path(dist: dict, prev: dict, target: str) -> iter:
	path = deque([],dist[target])
	u = target
	while dist[u]:
		path.appendleft(u)
		u = prev[u]
	return path
	
def get_closest_path(paths: dict, valves: dict, source: str, target: str) -> iter:
	# Try to get path from paths, else, adds to it
	key = source+target
	if not key in paths:
		# Calculating path and adding to paths 
		dist, prev = dijkstra(valves, source)
		path = dijkstra_path(dist, prev, target)
		paths[key] = path
	return paths[key]

	
def process_data() -> dict:
	# Loading data 
	with open("input.txt", "r") as f:
		data = f.read().strip().split("\n")

	# Parsing data 
	valve_pat = "([A-Z]{2})"
	rate_pat = "rate=(\d+)"
	valves = defaultdict(lambda : {"F": None, "in": [], "out": []})
	for line in data:
		valves_found = re.findall(valve_pat, line)
		rate_found = int(re.findall(rate_pat, line)[0])
		v = valves[valves_found[0]]
		v["out"] = valves_found[1:]
		v["F"] = rate_found
		for valve in v["out"]:
			valves[valve]["in"].append(valves_found[0])

	# Sorting the valves for convenience whilst making the default dict a diec
	valves = {v: valves[v] for v in sorted(valves)}
	
	# Adding open valves
	state = {"t": None}
	state["open"] = deque([v for v in valves if not valves[v]["F"]], len(valves))
	return valves, state
	
if __name__ == "__main__":
	main()


