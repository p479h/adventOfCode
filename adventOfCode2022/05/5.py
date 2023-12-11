import re
from collections import defaultdict, deque

crates, moves = open("./input.txt").read().split("\n\n")

# Loading the create packages 
crates = [[c for c in r[-2::-1] if c!=" "] for r in list(zip(*crates.splitlines()))[1::4]]
moves = [tuple(map(int,re.findall("(\d+)",l))) for l in moves.splitlines()]

# Moving the packages 
crates2 = list(map(list,crates))
for amount, from_, to_ in moves:
    from_, to_ = from_ -1, to_ -1 # Correct indices
    for _ in range(amount):
        crates[to_].append(crates[from_].pop())

    crates2[to_].extend(crates2[from_][-amount:])
    del crates2[from_][-amount:]

print("".join(c[-1] for c in crates))
print("".join(c[-1] for c in crates2 if c))