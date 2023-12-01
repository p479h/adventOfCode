"""
	Change in strategy.
	Travel through the air! 
		If cube neighbours air, add SA.
	Else:
		Search neighbours of neighbour
		
	Only reachable surfaces will be searched!
"""
from itertools import combinations

# Loading data 
with open("./inputs/input.txt", "r") as f:
	data = list(tuple(map(int, l.split(","))) for l in f.read().strip().split("\n"))
	cubes = data

# Getting outermost coordinates or AIR!
minout = tuple(min(p[i]-1 for p in data) for i in range(3))
maxout = tuple(max(p[i]+1 for p in data) for i in range(3))

# Function that checks if coordinate is iside domain
def inside_domain(cube: iter) -> bool:
	return all(minout[i]<=cube[i]<=maxout[i] for i in range(3))
	
# Function that gives all neighbours of cube
def neighbours(cube: iter) -> iter:
	return (tuple(cube[j]+int(i==j)*s for j in range(3)) for i in range(3) for s in (-1, 1))
	
# Defining variables and starting the search
cube = tuple(maxout)# Copy of cube for starting position
SA = 0 # Starting surface area 
queue = [cube]
seen = set()
while queue:
	cube = queue.pop()
	# Add surface area if cube is lava
	if cube in cubes:
		SA += 1
		continue # Should not find neighbours of solid
	if cube not in seen: # Add its neighbours to the queue and keep searching
		seen.add(cube)
		for n in neighbours(cube):
			if inside_domain(n):
				queue.append(n)
print(SA)

