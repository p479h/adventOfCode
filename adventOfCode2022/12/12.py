import matplotlib.pyplot as plt
from arrows_and_moves import MOVES
from collections import deque, defaultdict
from string import ascii_lowercase as LETTERS

with open('input.txt', "r") as f:
	t = f.read().strip()
	
# Getting height map as letters 
hml = [list(l) for l in t.split("\n")] 


# Getting dimensions of height map
H, W = len(hml), len(hml[0])


# Getting indices of S and E
tline = t.replace("\n", "")
Ei = tline.index("E")
Si = tline.index("S")
Ei2d = Ei//W, Ei%W
Si2d = Si//W, Si%W

# Replacing E and S by a and z
hml[Ei2d[0]][Ei2d[1]] = "z"
hml[Si2d[0]][Si2d[1]] = "a"

# Getting heiht map as heights
hm = deque([
	deque([LETTERS.index(hml[i][j]) for j in range(W)] ,W) for i in range(H)
	],H)


# Performing Dijkstra's algorithm
def Dijkstra(source):
	# Getting the neighbour lists, distances up until that point
	neighbours = defaultdict(lambda: deque([],4)) # Using linear indices!
	dist = {}
	prev = {}
	unvisited = deque([], H*W)
	for i, row in enumerate(hm):
		for j, height in enumerate(row):
			# Creating 2d index 
			IJ = i*W + j
			# Setting corresponding dist to high number and prev to undefined 
			dist[IJ] = float("inf")
			prev[IJ] = None
			unvisited.append(IJ)
			for option, move in MOVES.items():
				dy, dx = move
				y, x = i + dy, j + dx
				YX = y*W + x
				# Checking if neighbour in bounds
				if not ((-1<y<H) and (-1<x<W)):
					continue 
				# Checking height difference to neighbour
				height2 = hm[y][x]
				if height2-height <= 1: # Close enough, add to neighbour list
					neighbours[IJ].append(YX) 
					
	#source = Si
	dist[source] = 0
	while unvisited:
		u = min(unvisited, key=lambda d: dist[d])
		unvisited.remove(u)
		
		for neighbour in (set(neighbours[u]) & set(unvisited)):
			alt = dist[u] + 1
			if alt < dist[neighbour]:
				dist[neighbour] = alt
				prev[neighbour] = u
	return prev, dist

# Finding the best path (part 2)
m = 1e9
PREV = None
DIST = None
for IJ in range(H*W):
	i, j = IJ//W, IJ%W
	if hm[i][j] == 0: # a
		prev, dist = Dijkstra(IJ)
		if dist[Ei] < m:
			m = dist[Ei]
			PREV = prev
			DIST = dist

print(m)

# Visualizing the distances 
dst = deque([deque([-1]*W,W) for _ in range(H)],H)
for i, row in enumerate(dst):
	for j, count in enumerate(row):
		IJ = i*W + j
		if DIST[IJ] < 1e8:
			dst[i][j] = DIST[IJ]

plt.imshow(dst)
plt.contour(dst, levels = 26)

# Visualizing the path!
I = Ei
X = deque([], dist[Ei]+10)
Y = deque([], dist[Ei]+10)
while PREV[I]:
	i, j = PREV[I]//W, PREV[I]%W
	X.append(j)
	Y.append(i)
	I = PREV[I]
plt.plot(X, Y)
plt.show()
	
	
