# importing relevant libraries 
from collections import deque 
import matplotlib.pyplot as plt 

with open('input.txt', "r") as f:
	pathst = f.read().strip().split("\n") # Text paths
	paths = [[[int(x) for x in xy.split(",")] for xy in p.split(" -> ")] for p in pathst]

# Defining function to center the system 	
def center_system(paths: iter, left_top: iter):
	return [[[p[0]-left_top[0], p[1]-left_top[1]] for p in path] for path in paths]
	
def plot_walls(paths: iter) -> None:
	for p in paths:
		plt.plot(*list(zip(*p)), lw = 1, color = "cornflowerblue")
		
def fill_grid(grid: iter, path: iter) -> iter:
	# emptying the grid
	for row in grid:
		for index, col in enumerate(row):
			row[index] = "."
			
	# Assigning walls 
	for path in paths:
		for i, end in enumerate(path[1:], start = 1):
			 # Getting line information
			start = path[i-1]
			disp = [e - s for e, s in zip(end, start)]
			unit = [int(d/abs(d)) if d else 0 for d in disp]
			pos = [s for s in start]
			# Drawing the line
			while any(p!=e for p,e in zip(pos, end)):
				x, y = pos
				grid[y][x] = "#"
				pos[0] += unit[0]
				pos[1] += unit[1]
			grid[end[1]][end[0]] = "#"
	return grid

def display_grid(grid: iter) -> None:
	print(*["".join(g) for g in grid], sep = "\n")
	
def make_grid(path: iter, W: int, H: int) -> iter:
	# Creating sandgrid (more efficient than storing points and looping over them)
	grid = deque([deque(["."]*W,W) for _ in range(H)], H)

	# Filling in the grid 
	filled_grid = fill_grid(grid, paths)
	return grid
	
def lower_sandpoint(grid: iter, sandpoint: iter) -> iter:
	# Returns lowest index before hitting something
	x, y = sandpoint
	while grid[y+1][x] == ".":
		y += 1
	return x, y
	
def move_sideway(grid: iter, sandpoint: iter) -> iter:
	H, W = len(grid), len(grid[0])
	x, y = sandpoint
	# Try left, then right. If none work, return False
	if y+1 == H: # Can't fall lower
		return None
	elif x == 0: #If falls left, it falls forever
		return None 
	elif x > 0 and grid[y+1][x-1] == ".":
		return x-1, y+1
	elif x < W-1 and grid[y+1][x+1] == ".":
		return x+1, y+1
	else:
		return False
		
def get_dimensions(paths: iter, sandpoint: iter):
	minx = min(pair[0] for path in paths for pair in path)
	miny = min(pair[1] for path in paths for pair in path)
	maxx = max(pair[0] for path in paths for pair in path)
	maxy = max(pair[1] for path in paths for pair in path)

	# Getting important points for centering of system (aesthetics + easier indexing)
	top_left = [minx, miny]
	bottom_right = [maxx, maxy]
	W, H = maxx - minx+1, maxy-miny+1
	return W, H, top_left, bottom_right

def simulate(grid: iter, sandpoint: iter) -> None:
	# Getting grid dimensions 
	H: int = len(grid)
	W: int = len(grid[0])
	
	# Adding grain
	for i in range(100000):
		p = tuple(pp for pp in sandpoint)
		# Move down and sideways untill limit
		while 1:
			# Move p down
			p = lower_sandpoint(grid, p)
			# Try moving to sides 
			pnew = move_sideway(grid, p)
			if not pnew: # Finally the point is at rest
				if all(pp == ss for pp, ss in zip(p, sandpoint)): # Pyramid made!
					pnew = None
				break
			else:
				p = pnew
			
		x, y = p
		grid[y][x] = "o"
		if pnew is None:
			print(i+1)
			break
		

# Getting corners of coordinate system 
sandpoint = [[[500, 0]]]
paths = sandpoint+paths
W, H, top_left, bottom_right = get_dimensions(paths, sandpoint)
if True: # Add bottom path
	padx = W
	pady = 1
	new_path = [[[sandpoint[0][0][0]-W-padx, H+pady],[sandpoint[0][0][0]+W+padx, H+pady]]]
	paths = paths + new_path
	W, H, top_left, bottom_right = get_dimensions(paths, sandpoint)
	
# Getting centered system + sandpoint 
paths = center_system(paths, top_left)
sandpoint, paths = paths[0][0], paths[1:]

# Making grid
grid = make_grid(paths, W, H)

# Performing simulation
simulate(grid, sandpoint)

# display result
display_grid(grid)

# Plotting walls so we can see them
plot = False
if plot:
	plot_walls(paths)
	plt.plot([sandpoint[0]], [sandpoint[1]], marker="*", color="green")
	plt.gca().set_aspect("equal")
	plt.gca().invert_yaxis()
	plt.show()
