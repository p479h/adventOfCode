import re 
from math import prod
from itertools import chain, batched, combinations

in_ranges = lambda n, R: any(n in r for r in R)
all_in_ranges = lambda N, R: all(in_ranges(n, R) for n in N)

# Parsing input
text = open("data.txt").read()
ranges = {
    f: [range(i,j+1) for i,j in batched(map(int,l), 2)]
    for f,*l in re.findall(r'([\w ]+): (\d+)-(\d+) or (\d+)-(\d+)', text)
}
all_ranges = tuple(chain(*ranges.values()))
*rows, = map(eval, re.findall(r'^([\d,]+)', text, re.MULTILINE))

# Part 1
print(sum((n for n in chain(*rows[1:]) 
            if not in_ranges(n, all_ranges))))
    
# Part 2
# Discarding wrong rows and transposing
*columns, = zip(*[r for r in rows if all_in_ranges(r, all_ranges)])

# Making sets of plausible indices per field
indices = {
    f: {
        i for i,c in enumerate(columns) 
        if all_in_ranges(c,R)
    } 
    for f,R in ranges.items()
}

# Sorting so process of elimination is easier (first element will have single option, second 2 with one in common with previous, etc.)
indices = {k: indices[k] for k in sorted(indices, key = lambda s: len(indices[s]))}

# Elimination of indices 
for (_,i_set),(g,_) in combinations(indices.items(), 2):
    indices[g] -= i_set

print(prod(rows[0][s.pop()] for k,s in indices.items() if k.startswith('departure')))
