from itertools import product, permutations
data = list(list(map(int, l.strip())) for l in open("./input/input.txt"))
ny, nx = len(data), len(data[0])
adjp = tuple(permutations((-1, 0, 1), 2))+((1, 1),(-1,-1))
fadj = lambda I,J: tuple((I+i,J+j) for i,j in adjp if -1<I+i<ny and -1<J+j<nx)

def step(levels: iter) -> None:
	blew = []
	queue = [] # Those which can explode
	for i,j in product(range(ny), range(nx)): # Increasing all the levels by 1
		levels[i][j]+=1
		if levels[i][j] > 9: # Adding to explosion queue
			queue.append((i,j))
	while queue: # Allowing explosions
		ij = queue.pop() # One explosion at ta time
		i,j = ij
		if ij in blew: # Do not allow repeated explosions
			continue
		if levels[i][j] > 9: # Exploded
			blew.append(ij)
			for ni,nj in fadj(i,j): # Increase neighbours
				levels[ni][nj] += 1
				if levels[ni][nj] > 9 and not (ni,nj) in blew:
					queue.append((ni,nj))
	# Resetting exploded to 0
	for i,j in blew:
		levels[i][j] = 0
	return len(blew)
total = 0
for i in range(800):
	v = step(data)
	total += v
	if v == nx*ny:
		break
print(*data, sep="\n")
print(total)
print(i+1)
				
