import operator as op
import functools as ft 

# Loading the data 
t = tuple(tuple(map(int,l)) for l in open("./input.txt").read().splitlines())
tT = tuple(zip(*t))

# Set of all trees 
visible = {(i,j,c) for i,row in enumerate(t) for j,c in enumerate(row)}
scores = tuple([[0,0,0,0] for _ in r] for r in t) 
for (i,j,h) in tuple(visible):
    directions = (tT[j][:i][::-1] or [-1], tT[j][i+1:] or [-1], # Top bottom left right
                   t[i][:j][::-1] or [-1],  t[i][j+1:] or [-1])
    
    # Remove obstructed trees 
    if all(v>=h for v in map(max, directions)):
        visible.remove((i,j,h))
    
    # Count the score
    for di, d in enumerate(directions):
        for nh in d:
            scores[i][j][di] += 1 
            if nh >= h: 
                break

print(len(visible))
print(max(ft.reduce(op.mul,c) for r in scores for c in r))