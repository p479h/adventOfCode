import re 
import time 
import numpy as np
import matplotlib.pyplot as plt 

def main():
	m = simulate_blueprint(1, use_input = False, t = 24)
	print(m)
	
def simulate_blueprint(i: int, use_input: bool = False, t: int = 24):
	geomax = 0
	bank = np.array([0, 0, 0, 0], int) # ore caly obs in possession
	robots = np.array([1, 0, 0, 0], int) # Number of robots in stock
	blueprints = load_blueprints(use_input)
	costs = load_blueprint(blueprints[i])
	MAX = [0]
	tree_blueprint(bank, robots, costs, t, MAX)
	return MAX[0]
	
def tree_blueprint(
	bank: np.ndarray, 
	robots: np.ndarray, 
	costs: np.ndarray, 
	t: int,
	MAX: iter = [0],
	) -> int:
	# Check if the current value is maximum
	MAX[0] = max(MAX[0], bank[-1])
	
	# Stops branch if necessary
	if should_stop_branch(bank, robots, costs, t, MAX):
		return
		
	# Check things that can be bought. Buy one of each or None
	can_afford = can_buy(bank, costs).astype(int)
	
	# Either buy nothing or one of each option
	i_amount = tuple((i, amount) for i, amount in enumerate(can_afford) if amount) + ((0, 0),) 

	# IF you have 0 of a robot that you can build, build it!
	for i, amount in i_amount:
		if robots[i] == 0 and amount:
			i_amount = tuple(im for im in i_amount if robots[im[0]]==0 and im[1])
			break
	
	# Always build geode robot if possible!
	if (3, 1) in i_amount:
		i_amount = ((3, 1),)
		
	for i, amount in i_amount:
		# Start building 
		bank -= costs[i]*amount
		
		# Each robot collects their take!
		bank += robots # One of each ore for each robot
		
		# Finish building robot
		robots[i] += amount
		
		# With current setup, go to the next simulation step
		tree_blueprint(bank, robots, costs, t-1, MAX)
		
		# Return simulation to original state
		robots[i] -= amount
		bank -= robots
		bank += costs[i]*amount
				
def should_stop_branch(bank: np.ndarray, robots: np.ndarray, costs: np.ndarray, t: int, MAX: iter) -> bool:
	# Checking if current branch can possibly generate more geode assuming 1 geode robot a day
	# t -> geoges 
	# 1 -> nr*t + 0
	# 2 -> nr*t + 1 + 0
	# 3 -> nt*t + 2 + 1 + 0
	# 4 -> nt*t + 3 + 2 + 1 +0
	max_geodes = bank[-1] + robots[-1]*t + sum(i for i in range(t))
	if max_geodes <= MAX[0]:
		return True 
	
	# Do not build too many robots
	# IF the most expensive robot costs n of j, do not have more than n j robots
	mincosts = tuple(min(c for c in cost if c) for cost in costs[:, :-1].T)
	for ir, nr in enumerate(robots[:3]):
		if nr-1 > mincosts[ir]:
			return True
			
	# If there is too much in the bank!
	if any(b/r > 30 for b,r in zip(bank, robots) if r > 0) or np.any(bank > 60):
		return True
		
		
	## If time is out
	if not t:
		return True
		
	# If all else fails
	return False
	
	
def selective_bin_count(arr:iter = None, i: int = 0, n: int = 3):
	if arr is None:
		arr = [0 for _ in range(n)]
	if i < n and arr[i]:
		for value in (0, 1):
			arr[i] = value
			yield from selective_bin_count(arr, i+1, len(arr))
	elif i < n: # And not arr[i]
		yield from selective_bin_count(arr, i+1, len(arr))
	else:
		yield arr
	
def can_buy(bank: np.ndarray, cost: np.ndarray) -> np.ndarray:
	return np.all(bank>=cost, axis = 1)

def load_blueprint(blueprint: str) -> dict:
	# robots 
	# ore clay obsidian geode-> [0-3]

	# Defining partterns to get costs 
	ore_pat = r"ore robot costs (\d+) ore"
	cla_pat = r"clay robot costs (\d+) ore"
	obs_pat = r"obsidian robot costs (\d+) ore and (\d+) clay"
	geo_pat = r"geode robot costs (\d+) ore and (\d+) obsidian"
	
	# Loading costs
	ore_cost = int(re.search(ore_pat, blueprint).group(1))
	cla_cost = int(re.search(cla_pat, blueprint).group(1))
	obs_cost = tuple(map(int, re.search(obs_pat, blueprint).groups()))
	geo_cost = tuple(map(int, re.search(geo_pat, blueprint).groups()))

	# Defining cost matrix # robot vs price of ore clay obsidian
	costs = np.zeros((4, 4), int)
	costs[0,0] = ore_cost # Ore robot costs ore! (0,)
	costs[1,0] = cla_cost # Note that clay robot costs ORE not clay! (0,)
	costs[2,:2] = obs_cost # Costs ore and clay (0, 1)
	costs[3,[0, 2]] = geo_cost
	return costs
	

# Loading blueprints 
def load_blueprints(use_input: bool = False):
	filename = "./inputs/%s.txt" % ("input" if use_input else "example")
	with open(filename, "r") as f:
		return f.read().strip().split("\n")
	
if __name__ == "__main__":
	main()
