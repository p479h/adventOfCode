def flatten_(t):
	if type(t) in (int,float):
		yield t
	else:
		for e in t:
			yield from flatten(e)
			
def flatten(t):
	return list(flatten_(t))
		
def depthmap(t,depth=0,dmap=None): # NUmber is the flattened index of a number
	if dmap is None: 
		dmap = []
	if type(t) in (int, float):
		dmap.append(depth)
	else:
		for i,e in enumerate(t):
			depthmap(e,depth+1,dmap)
	return dmap
	
def shapeback(flat,dmap,depth=1):
	v = []
	stack = [v] # Last element is the current layer!
	for e,d in zip(flat,dmap):
		while len(stack[-1]) == 2:
			stack.pop()
			depth -= 1
		while d > depth: # Must create deeper array
			depth += 1 # Increasing depth counter
			stack[-1].append([]) # Adding new layer to v
			stack.append(stack[-1][-1]) # Adding that same layer to stack
		while depth > d:
			stack.pop() # Removing last layer from stack
			depth -= 1 # Decreasing the depth
		stack[-1].append(e) # Adding the element to v through the stack
	return v
	
def split(flat, dmap, i):
	d = flat[i]//2 # Rounded down 
	u = flat[i] - d # Rounded up
	flat[i] = u # Substituting number by split
	dmap[i] += 1 # Increasing the depth
	flat.insert(i,d)
	dmap.insert(i,dmap[i])

def explode(flat,dmap,i): # i is the index of first element of pair
	# Left number 
	DI = [-1,1]
	for stride,di in enumerate(DI):
		if -1<stride+i+di<len(flat): # If there is a neighbour
			flat[stride+i+di] += flat[stride+i]
	# Removing the pair
	flat.pop(i)
	dmap.pop(i)
	flat[i] = 0
	dmap[i]-= 1
	
def add(t1,t2):
	return [t1,t2]

def addmany(*t):
	if len(t) == 1:
		return reduce(t[0])
	return reduce([addmany(*t[:-1]),t[-1]])

def reduce(row):
	dmap = depthmap(row)
	flat = flatten(row)
	while any(d>4 or e>9 for d,e in zip(dmap,flat)):
		for i,d in enumerate(dmap):
			if d>4: 
				explode(flat,dmap,i)
				break
		else: # Only if not exploded
			for i,e in enumerate(flat):
				if e > 9:
					split(flat,dmap,i)
					break # So dmap can be tried
	tensor = shapeback(flat,dmap)
	return tensor

def mag(t):
	if type(t) in (int,float):
		return t
	return 3*mag(t[0])+2*mag(t[1])

table = tuple(eval(line.strip()) for line in open("./input/input.txt"))
row = addmany(*table)
m = mag(row)
print(m)

# Part 2
from itertools import permutations
sums = tuple(mag(addmany(*c)) for c in permutations(table,2))
print(max(sums)) 

