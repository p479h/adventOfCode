from collections import Counter 
from itertools import accumulate # Could also use reduce 

data, cwd = open("./input.txt"), []
space = Counter()
for l in map(str.split, data):
    match l: # Learned the match statement from 4HbQ on reddit
        case "$", "cd", "..":
            cwd.pop()
        case "$", "cd", d: 
            cwd.append(d)
        case size, _ if size.isdigit(): 
            for d in accumulate(cwd): 
                space[d] += int(size)
# Part 1
print(sum(s for s in space.values() if s<=1e5))

# Part 2
print(min(v for v in space.values() if v>=3e7-(7e7-space["/"] )))