lines = tuple(l.strip() for l in open("./input/input.txt"))

# Function that finds all groups of parenthesis
op = "(","[","{","<"
cl = ")","]","}",">"
points = {k:v for k,v in zip(cl,[3, 57, 1197, 25137])}
def find_error(s: str, return_points: bool = True) -> str:
	d = 0
	depth = [(s[0],0)] # Character used to open
	for c in s[1:]:
		if c in op: # If opening bracket
			d += 1
			depth.append((c,d))
		else: # Closing bracket
			last,dl = depth.pop()
			# If the closing bracket is different, at the closing, thats the mistake
			if op.index(last) != cl.index(c):
				return points[c]
			else: # Decrease depth if exited the 
				d -= 1
	if return_points:
		return 0
	return depth 

s = sum(find_error(l) for l in lines)

# Part 2
def discard_corrupted(lines: iter) -> iter:
	for l in lines:
		error = find_error(l, return_points=True)
		if not error:
			yield l

scores = []
clean = tuple(discard_corrupted(lines))
points2 = {k:v for k,v in zip(cl,[1, 2, 3, 4])}
for c in clean:
	p = 0
	depth = find_error(c, return_points = False)
	missing = [cl[op.index(depth.pop()[0])] for _ in range(len(depth))]
	for m in missing:
		p*=5
		p+=points2[m]
	scores.append(p)
score = sorted(scores)[len(scores)//2]
print(score)
