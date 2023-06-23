import numpy as np
from itertools import combinations
from collections import defaultdict

# Defining number of coordinates
NDIM = 2

# Loading data 
data = [[tuple(map(int,c.split(","))) 
		for c in l.split("\n")[1:] if c] 
		for l in open("./input/example.txt").read().split("\n\n")]
		
# Computing manhatan distances as identifiers!
ds = []
for si,l in enumerate(data): #Looping over scaners
	ds.append([]) 
	for (i0,c0), (i1,c1) in combinations(enumerate(l),2): # Looping over coordinates
		d = [abs(c0[i]-c1[i]) for i in range(NDIM)]
		v = [(i0,i1),(sum(d),min(d),max(d))]
		ds[-1].append(v)
		
		
print(ds)
