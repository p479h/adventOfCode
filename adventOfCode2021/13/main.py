import re 
numbers, foldstxt = open("./input/input.txt").read().strip().split("\n\n")
dots = set(tuple(map(int,l.split(","))) for l in numbers.split("\n"))
folds = []
for f in foldstxt.split("\n"):
	value = int(re.search(r'\d+', f).group())
	folds.append((value,0) if "y" in f else (0, value))
for fold in folds:
	newdots = set()
	fx, fy = fold
	while dots:
		y,x = dots.pop()
		if fx and x > fx:
			x = 2*fx - x
		if fy and y > fy:
			y = 2*fy - y
		newdots |= {(y,x)}
	dots = newdots

mima = [[],[]]
for axis in (0,1):
	mima[0].append(min(a[axis] for a in dots))
	mima[1].append(max(a[axis] for a in dots))

dy, dx = mima[1][0] - mima[0][0] + 1, mima[1][1] - mima[0][1] + 1
arena = ["".join(["#" if (i,j) in dots else "." for j in range(dx)])for i in range(dy)]
print(*list("".join(a) for a in zip(*arena)), sep="\n")
print(len(dots))
