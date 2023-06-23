# Importing relevant libraries
import re 
import numpy as np
# THIS ANSWER WAS COPIED FROM REDDIT! There was no time for me to do it :(

# STRATEGY
# By taking the branches with most robots of a prespecified order
# one can eliminate branches without enough obs and geo robots.
# Avoid overhead by using loops + queue

# Function that makes it easier to define vector
V = lambda *a: np.array(a, int)

# Function to parse a given rem
def parse_blueprint(line: str):
	i, a, b, c, d, e, f = map(int, re.findall(r"\d+", line))
	return (i, ((V(0, 0, 0, a),V(0, 0, 0, 1)),
				(V(0, 0, 0, b),V(0, 0, 1, 0)),
				(V(0, 0, d, c),V(0, 1, 0, 0)),
				(V(0, f, 0, e),V(1, 0, 0, 0)),
				(V(0, 0, 0, 0),V(0, 0, 0, 0))))
		 #(bp index, (cost, production|robot count))

# Function to obtain sorting key
key = lambda a: tuple(a[0]+a[1])+tuple(a[1]) # All robot counts
# Helps sort by money+robots->money

# Function to get most relevant branches (most robots of obsidian|geo)
remove_duplos = lambda x: {key(x):x for x in x}.values()
prune = lambda x: sorted(remove_duplos(x), key = key, reverse=True)[:1000]


# Runs each time step at a time, adding best candidates to queue
def run(blueprint: tuple, t: int = 24) -> int:
	queue = [(V(0, 0, 0, 0), V(0, 0, 0, 1))]
	for t_ in range(t):
		temp_queue = []
		for have, make in queue:
			for cost, robot in blueprint:
				if all(cost <= have): # Adding possibility to queue 
					temp_queue.append((have+make-cost,make+robot))
					#          append((next saldo, next total number of robots))
		queue = prune(temp_queue)
	return max(have[0] for have, _ in queue) # Return the maximum number that we have from queue
	
# Opening files to get blueprints
# Part 1
p1 = 0
p2 = 1
bplines = open("inputs/input.txt", "r").read().strip().split("\n")
for line in bplines:
	i, bp = parse_blueprint(line)
	p1+= i*run(bp, 24)
	if i > 3: continue
	p2 *= run(bp, 32)
	
print(p1)
print(p2)
