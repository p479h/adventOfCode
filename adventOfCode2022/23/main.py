# Leading libraries
import numpy as np
from itertools import product

# Defining global variables
#		N		S		W		E	
MOVES = (-1, 0), (1, 0), (0, -1), (0, 1)

def main():
	field = parse_file("./input/example.txt")
	elves = make_elves(field)
	
	for i in range(10):
		update_elves(elves, field)
		#print(*elves, sep="\n")
		move_elves(elves, field)
	print(field)
	print()
	cropped = crop_field(field)
	print(cropped)
	print(np.sum(cropped == 0))
	print(np.sum(field == 0))
	
# Parsing the table
def parse_file(fname: str) -> np.ndarray:
	field = []
	for l in open(fname):
		if not l.strip():
			continue	
		field.append([{".":0,"#":1}[c] for c in l.strip()])
	return np.array(field)
	
	
def crop_field(field: iter) -> iter:
	alli = (slice(0, 1), slice(None, None))
	alle = (slice(-1, None), slice(None, None))
	ij = (slice(1,None),slice(None,None))
	ije = (slice(0, -1), slice(None, None))
	for dim in range(2):
		if dim:
			ij = ij[::-1]
			alli = alli[::-1]
			ije = ije[::-1]
			alle = alle[::-1]
		while np.all(field[alli]==0):
			field = field[ij]
		while np.all(field[alle] == 0):
			field = field[ije]
	return field

	
def make_elf(ij: iter) -> dict:
	# NSWE are the neighbour indices of NSWE
	elf = {"ij": ij, "NSWE": [0, 1, 2, 3], "next_movement": None, "next_ij": None}
	return elf

def make_elves(field: iter) -> iter:
	H,W = field.shape
	elves = []
	for i in range(H):
		for j in range(W):
			ij = i, j
			if field[ij]:
				elves.append(make_elf(ij))
	return elves

def get_direction(elf: dict, field: iter) -> iter:
	# Returns the index of the prefered direction to move!
	# Finding the indices where it can go!
	H, W = field.shape
	# Check for empty neighbourhood
	alln = list(product((0, 1, -1), repeat=2))[1:] # all neighbours
	IJ = tuple(tuple(m+e for m,e in zip(elf["ij"],n)) for n in alln)
	n = (ij for ij in IJ if (0 <= ij[0] < H and 0 <= ij[1] < W))
	if all(not field[ij] for ij in n):
		return None
	
	for movei in elf["NSWE"]: #Try move indices according to priority
		m0, m1 = MOVES[movei]
		for i, s in enumerate((-1, 0, 1)):
			move = (m0, m1+s) if m0 else (m0+s, m1)
			ij = tuple(m+e for m,e in zip(elf["ij"],move))
			if  not (0 <= ij[0] < H and 0 <= ij[1] < W):
				break
			elif field[ij]:
				break
		else: #return first successfull trial! (It function did not break)
			
			return movei # Move index which allows for movement	
	return None
		
def update_elf(elf: dict, field: iter) -> None:
	i = get_direction(elf, field)
	if not i is None: # If the elf can move
		move = MOVES[i]
		next_ij  = tuple(i+di for i, di in zip(elf["ij"], move))
		index = elf["NSWE"].index(i)
	else:
		move = None
		next_ij = None
	elf["NSWE"].append(elf["NSWE"].pop(0)) # moving to the end of priority
	elf["next_movement"] = move
	elf["next_ij"] = next_ij
	
	
		
	
def update_elves(elves: iter, field: iter) -> None:
	for elf in elves:
		update_elf(elf, field)
	# Removing intersecting end positions
	for i, elf0 in enumerate(elves[:-1]):
		next_ij = elf0["next_ij"]
		for elf1 in elves[i+1:]:
			if elf1["next_ij"] == next_ij: # If intersecting next positions, remove next movement
				for e in (elf0, elf1):
					e["next_ij"] = None
					e["next_movement"] = None

def move_elves(elves: iter, field: iter) -> None:
	for elf in elves:
		if elf["next_ij"] is None:
			continue
		field[elf["ij"]] = 0
		field[elf["next_ij"]] = 1
		elf["ij"] = elf["next_ij"]
		elf["nswe"] = elf["next_movement"] = None
		
		
	
if __name__ == "__main__":
	main()
