import time
import numpy as np
from collections import deque 
from shapes import Shape, Field
import matplotlib.pyplot as plt


def main():
	part2()
	
def part2():
	"""Look for cycles in patterns and do the math."""
	dh = 2685
	ds = 1725
	leftover = 1000000000000%ds
	field = simulate_nitter(leftover)
	h = max(field.h-s.x[1] for s in field.shapes)
	print(h + dh*(1000000000000//ds))
	
def measure_convergence():
	nitters = [10, 100, 2022, 4000]
	durations = []
	for nitter in nitters:
		s = time.time()
		field = simulate_nitter(nitter)
		durations.append(time.time()-s)
		
	plt.loglog(nitters, durations)
	plt.show()
	order,intercept = np.polyfit(np.log(nitters), np.log(durations), 1)
	print("The order of operations is approximately %.2f" % order)
	ni = 1000000000000
	t = np.exp(order*np.log(ni)+intercept)
	maxh = str(max(field.h-s.x[1] for s in field.shapes))
	print("With this, it would take %s s for %i operations" % (t, ni))
	print("It actually took %.2f s and highest object y = %s" % (durations[-1], maxh))		
		
def simulate_nitter(nitter: int = 10):
	# Defining global variables 
	nshapes = 5
	shapes = deque([Shape(i, [2, 0]) for i in range(nshapes)], nshapes)
	shape_gen = cycle_over_shapes(shapes) # Inifinite shape looper 
	move_gen = gen_movements("inputs/input.txt")
	field = Field([0, 0], 7, 10)
	simulate(field, move_gen, shape_gen, nitter)
	return field

	
def gen_movements(file: str) -> iter:
	moves = {">": [1, 0], "<": [-1, 0]}
	with open(file, "r") as f:
		arrows = f.read().strip()
	while True:
		for arrow in arrows:
			yield moves[arrow]

def cycle_over_shapes(shapes: iter):
	while True:
		for s in shapes:
			yield s

def simulate(field: "Field", moves: iter, shapes: iter, nitter: int = 100) -> None:
	while len(field.shapes) < nitter:
		new_shape = next(shapes).instantiate()
		field.add_shape(new_shape)
		field.move_shape_to_start(new_shape)
		field.update_bin(new_shape)
		while True:
			# Moving with gas 
			move = next(moves)
			new_shape += move
			
			# Checking for wall/shape overlap and moving back accordingly
			if new_shape.overlaps_wallsx(field) or new_shape.overlaps_shapes2(field):
				new_shape-=move
			
			# Moving down
			move = [0, 1]
			new_shape += move
			field.update_bin(new_shape)
			if new_shape.overlaps_shapes2(field) or new_shape.overlaps_wallsy(field):
				new_shape-=move
				field.update_bin(new_shape)
				break
	
	
if __name__ == "__main__":
	main()
	
