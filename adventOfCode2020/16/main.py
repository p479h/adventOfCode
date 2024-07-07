import re 
from itertools import chain

fields, _, nearby = open("test.txt").read().split("\n\n")
nearby = [tuple(map(int, l.split(","))) for l in nearby.splitlines()[1:]]
ranges = {
    re.search(r"\w+", l).group(): [range(int(a), int(b)+1) for a,b in re.findall(r"(\d+)-(\d+)", n)]
    for l, n in (f.split(":") for f in fields.splitlines())
}

# Part 1
print(sum((n for n in chain(*nearby) 
                if not any(n in r for r in chain(*ranges.values())))))
    
# Part 2
# Discarding wrong rows
print(nearby)
nearby = [l for l in nearby if all(any(n in r for r in chain(*ranges.values())) for n in l)] 
print(nearby)
                  