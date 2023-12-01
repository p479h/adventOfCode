# Importing relevant data types
import sys
sys.setrecursionlimit(1000)
from itertools import chain
from collections import defaultdict, Counter

# Parsing the pairs 
pairs = [l.strip().split("-") for l in open("./input/input.txt")]

# Making a dictionary with the connections
caves = defaultdict(lambda: [])
for c0, c1 in pairs:
	caves[c0].append(c1)
	caves[c1].append(c0)
caves = dict(caves)

# Searching neighbours of each cave
res = []
def search_end(s: str = "start", visited: iter = ["start"], path: iter = ["start"], nleft: int = 0, count=[0]):
	for n in caves[s]: # Looping through neigbours
		if n == "end":
			res.append(path+["end"])
			count[0]+=1	
			continue
		if n in visited: # Go to the next iteration
			continue
		if n.islower():
			for i in range(nleft+1): # i Will be 0, if nleft = 0 else 1!
				visited_ = visited + ([n] if i==0 else [])
				search_end(n, visited_, path+[n], nleft=nleft-i, count=count)
		else:
			search_end(n, visited, path+[n], nleft, count)
	return count[0]
	
#n = search_end()
#print(n)

# Part 2
n = search_end(nleft = 1) # 1 visit to small caves
print(len(set(tuple(r) for r in res)))
