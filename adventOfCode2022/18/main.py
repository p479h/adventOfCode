# Part 1
# loading example data 
with open("./inputs/input.txt", "r") as f:
	data = f.read().strip().split("\n")

points = [tuple(int(p) for p in l.split(",")) for l in data]
counts = {i: 0 for i in range(len(points))}
#xsort = sorted(points, key = lambda a: a[2])
#ysort = sorted(xsort, key = lambda a: a[1])
#zsort = sorted(ysort, key = lambda a: a[0])

# Making grids that facillitate finding neighbours
maxs = [max(p[i] for p in points) for i in range(3)]
mins = [min(p[i] for p in points) for i in range(3)]
Hx = maxs[2]-mins[2] + 1
Hy = maxs[1]-mins[1] + 1
Hz = maxs[0]-mins[0] + 1
		
xygrid= [[[] for _ in range(Hx)] for _ in range(Hy)]
yzgrid= [[[] for _ in range(Hy)] for _ in range(Hz)]
zxgrid= [[[] for _ in range(Hz)] for _ in range(Hx)]

# Filling up grids
for I, P in enumerate(points):
	i, j, k = [zyx-mi for zyx, mi in zip(P, mins)] # Getting grid indices
	xygrid[j][k].append(I)
	yzgrid[i][j].append(I)
	zxgrid[k][i].append(I)

# Sorting based on each coordinate
for i in range(3):
	grid = (xygrid, zxgrid, yzgrid)[i]
	for ii, row in enumerate(grid):
		for jj, col in enumerate(row):
			zyxpoints = [zyx[i] for zyx in points] # Extracting correct coordinate
			grid[ii][jj] = sorted(col, key=lambda a: zyxpoints[a])
			for ip in range(1,len(grid[ii][jj])):
				p0, p1 = grid[ii][jj][ip-1], grid[ii][jj][ip]
				p0, p1 = zyxpoints[p0], zyxpoints[p1]
				if abs(p0-p1) == 1:
					counts[ip]+=1
					counts[ip-1]+=1
#print(yzgrid)
# Computing surface area
SA = len(points)*6
for c in counts.values():
	SA -= c
print(SA)
#print(*zsort, sep="\n")
