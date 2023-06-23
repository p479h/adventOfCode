# Loading relevant libraries
import re 
from functools import reduce
from collections import deque
from itertools import chain, product

def load_field() -> iter:
	digit = r"(-?\d+)"
	pat = r"Sensor at x=%s, y=%s: closest beacon is at x=%s, y=%s" % ((digit,)*4)
	pattern = re.compile(pat)
	with open("input.txt", "r") as f:
		Map = pattern.findall(f.read().strip())
	pairs = map(lambda e: (tuple(int(i) for i in e[:2]),tuple(int(i) for i in e[2:])), Map)
	sensors, beacons = list(zip(*pairs))
	return sensors, beacons
	
def search_row(row: int, sensor: iter, d: int):
	# Computing remaining available displacements 
	dy = abs(row - sensor[1])
	rem = d - dy
	# If none left, return empty tuple
	if rem < 0:
		return set()
	#print(sensor[0], rem)
	return set(i for i in range(sensor[0]-rem, sensor[0]+rem+1))
	
def get_impossible_row(row: int, sensors: iter, beacons: iter, disps: iter) -> set:
	not_possible = set()
	for s, b, d in zip(sensors, beacons, disps):
		not_possible |= search_row(row, s, d)
	return not_possible
	
def in_range(s: iter, p: iter, d: int) -> bool:
	return sum(abs(pp-ss) for pp, ss in zip(s, p)) <= d
	

def get_perimeter(point: iter, d: int, lim: iter = None) -> iter:
	x, y = point
	y += d
	dx = [1, -1, -1, 1]
	dy = [-1, -1, 1, 1]
	for s in range(4):
		for _ in range(d):
			if lim is None or all(lim[0]<=p<=lim[1] for p in (x, y)):
				yield x, y
			x += dx[s]
			y += dy[s]

	
# Loading the field, then getting search "radius"
sensors, beacons = load_field()
disps = tuple(sum(abs(b-s) for b, s in zip(B, S)) for B, S in zip(sensors, beacons))

# Part 1
row = 2000000
not_possible = get_impossible_row(row, sensors, beacons, disps)

# removing the positions of beacons and sensors
not_possible -= set(x for x, y in chain(sensors+beacons) if y == row)

print(len(not_possible))

# Part 2
# Getting the row map limits
lim = (0, 4000000+1)

# Getting outer perimeters of the sensors 
perimeters = (get_perimeter(s, d+1, lim) for s, d in zip(sensors, disps))

# Keep those points that are not in range of another sensor
clean_perimeters = tuple(set(point for point in p if not any(in_range(point, s, d) for s, d in zip(sensors, disps))) for p in perimeters)

# The point we are looking for is in the outer perimeter of more than one sensor
for i in range(len(clean_perimeters) - 1):
	for j in range(i+1, len(clean_perimeters)):
		overlap = clean_perimeters[i]&clean_perimeters[j]
		if overlap:
			break
	else:
		continue # If no result found, continue to the next iteration
	overlap = tuple(overlap)
	print(overlap[0]*4000000+overlap[1])
	break

# Print the points


