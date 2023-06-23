from collections import deque 

def to_height(field: iter) -> iter:
	# Find field dimensions
	h = len(field)
	w = len(field[0])
	
	# Allocating memory
	hm = deque([deque([], w) for _ in range(h)],h)	
