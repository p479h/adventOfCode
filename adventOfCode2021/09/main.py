from itertools import product
data = list(list(map(int,l.strip())) for l in open("./input/input.txt"))
ny, nx = len(data), len(data[0])
MOVES = ((-1, 0),(0, 1),(1, 0),(0, -1)) # N E S W
diff = lambda a,b: a-b
fneighs = lambda I,J: tuple((I+i,J+j) for i,j in MOVES if -1<I+i<ny and -1<J+j<nx)
hneighs = lambda A, I,J: tuple(diff(A[I][J],A[In][Jn]) for In,Jn in fneighs(I,J))
ans = sum(1 + data[i][j] if all(hd <= 0 for hd in hneighs(data,i,j)) else 0 for i,j in product(range(ny),range(nx)))
print(ans)

# Part 2
# Find all low points
basins = list((i,j) for i,j in product(range(ny),range(nx)) if all(hd < 0 for hd in hneighs(data,i,j)))
contained = [[]] # Points for each basin

#Search their neighbours
queue = [basins.pop(0)]
visited = []
visited.append(queue[0])
while True:
	ij = queue.pop(0)
	contained[-1].append(ij)
	for ijn in fneighs(*ij): # Adding its neighbours to queue
		if data[ijn[0]][ijn[1]] < 9 and not  ijn in visited:
			queue.append(ijn)
			visited.append(ijn)
		
	if len(queue) == 0: # No more neighbours under 9
		if len(basins) == 0: # No more basins as starting points
			break
		queue.append(basins.pop())
		visited.append(queue[0])
		contained.append([])

sizes = sorted(map(len, contained))
a,b,c = sizes[-3:]
print(a*b*c)
