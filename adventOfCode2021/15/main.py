# Loading the data
data = tuple(tuple(map(int,l.strip())) for l in open("./input/input.txt"))
ny, nx = len(data), len(data[0])
points = {(i,j):data[i][j] for i,_ in enumerate(data) for j,_ in enumerate(data[0])}

# Function to find the available neighbours
MOVES = ((-1,0),(0, 1),(1,0),(0,-1))
def fneighbours(ij, ny: int = ny, nx: int = nx):
	i, j = ij
	for mi,mj in MOVES:
		if -1<i+mi<ny and -1<j+mj<nx:
			yield (i+mi,j+mj)

def dijkstra(points, S=(0,0), E=(ny-1, nx-1), ny: int = ny, nx: int = nx):
	# Do a search based on distance
	queue = set(points)
	seen = set([S])
	dist = {S:0} # Distances to each spot
	prev = {S:None}
	for n in points: #Initializing the dist and prev dicts
		if n != (0, 0):
			dist[n] = 1e10
			prev[n] = None
		
	while queue: # Run until queue is empty!
		s = min(queue&seen, key=lambda ij: dist[ij])
		queue.remove(s)
		for n in fneighbours(s, ny, nx):
			if not n in queue or n in seen: continue
			seen|={n}
			dn = dist[s] + points[n] # Distance walking through s
			if dist[n] > dn: # Replace the bad path by a better one
				dist[n] = dn
				prev[n] = s
				
	#print(dist)
	print(dist[E])

#dijkstra(points)
# Part 2
# Updating points 
import time
s = time.time()
N = 5
pcopy = points.copy()
for i in range(N):
	for j in range(N):
		for ij, v in pcopy.items():
			I = ij[0]+i*ny
			J = ij[1]+j*nx
			V = (v+i+j-1)%9+1
			if not V: V = 1
			points[(I,J)] = V
			
E = (ny*N-1, nx*N-1)
S = (0, 0)
dijkstra(points, S, E, ny*N, nx*N)
print(time.time()-s)
