import numpy as np

# Missing part 2!!! Time issues 

def main():
	MAP, path = load_data()
	d, p = find_start(MAP) # Starting position from left top corner
	x = (d, p) # direction, position
	path = process_path(path) # Making path iterable
	temp = [list(l) for l in MAP]
	
	for step in path:
		move_step(MAP, step, x, temp)
	print(x2points(x))
	for l in temp:
		print("".join(l))
	print(path)
	
def x2points(x):
	facing = {(1, 0):0,(0, 1):1,(-1, 0):2,(0, -1):3}[tuple(x[0])]
	return 1000*(x[1][1]+1) + 4*(x[1][0]+1) + facing
	
	
def move_step(MAP: iter, step: iter, x: iter, temp = None):
	move, rotation = step
	d, p = x # direction, position
	count = move # Number of steps
	dimension = np.where(d!=0)[0][0]
	if dimension: # y
		strip = [xstrip[p[0]] if p[0] < len(xstrip) else " " for xstrip in MAP]
	else:
		strip = MAP[p[1]]
	l = len(strip)
	
	if temp:
		char = {(1, 0):">",(0, 1):"v",(-1, 0):"<",(0, -1):"^"}[tuple(d)]
		j, i = p
		temp[i][j] = char
		
	while count:
		count -= 1
		pnew = p + d
		pnew[dimension] %= l
		while strip[pnew[dimension]] == " ":# If crossed a boundary, keep going!
			pnew += d
			pnew[dimension] %= l
		if strip[pnew[dimension]] == "#": # hit a wall!
			break
		# If # and " " are not active, pnew must lie on a dot!
		p[:] = pnew
		if temp:
			char = {(1, 0):">",(0, 1):"v",(-1, 0):"<",(0, -1):"^"}[tuple(d)]
			j, i = p
			temp[i][j] = char

	# Rotating the direction vector!
	d[:] = turn(rotation, d)
	if temp:
		char = {(1, 0):">",(0, 1):"v",(-1, 0):"<",(0, -1):"^"}[tuple(d)]
		j, i = p
		temp[i][j] = char		
	
#Finding starting position (0-l)
def find_start(MAP):
	y = 0
	x = MAP[0].index(".")
	return np.array([1, 0], int), np.array([x, y], int)
	
# Turn function 
def turn(direction: str, d: np.ndarray):
	R = np.array([[0, -1],[1, 0]], int)
	if direction == "L":
		R*=-1
	elif direction != "R": #Don't rotate if unknown
		return d
	return R@d
	
# Extracting displacement
def get_disp(path: str):
	v = ""
	while path and path[0].isnumeric():
		v = v+path[0]
		path = path[1:] # extract leading character
	return int(v),path

# Extracting direction
def get_dirc(path: str):
	v = ""
	while path and not path[0].isnumeric():
		v= v+path[0]
		path = path[1:]
	return v, path
	
# Processing path
def process_path(path):
	PATH = []
	while path:
		if path[0].isnumeric():
			d, path = get_disp(path)
		else:
			d, path = get_dirc(path)
		PATH.append(d)
	path = list((d0, d1) for d0, d1 in zip(PATH[::2], PATH[1::2]))
	if len(path) < len(PATH) / 2:
		path.append((d, "None")) # No rotation in last walk
	return path

# Loading the data 
def load_data():
	MAP = []
	for l in open("./input/input.txt"):
		l = l.strip("\n")
		if "." in l:
			MAP.append(l)
		elif l:
			path = l
			
	return MAP, path
	
	
if __name__ == "__main__":
	main()
