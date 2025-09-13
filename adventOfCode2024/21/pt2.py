# Looked at 4Hbq's logic on reddit. Dijkstra route was too slow and verbose :(
from numpy import polyfit, polyval

lines = open("data.txt").read().splitlines()
garden = list(map(list, lines))

# Getting garden dimensions
h, w = map(len, (garden, garden[0]))
# Function to go back to a new line
cmod = lambda c: complex(c.real%h, c.imag%w)

G = set(complex(i,j) for i,r in enumerate(garden) 
                     for j,c in enumerate(r) if c!="#")
Q = {complex(i,j) for i,r in enumerate(garden) 
                     for j,c in enumerate(r) if c=="S"}

y = []
x = []
for it in range(4*w+1):
    if it == 64:
        print("Part 1: %i"%len(Q))
    q = (ij+d for d in (0+1j, 0-1j, 1+0j, -1+0j) for ij in Q) # Contestants 
    if not (it-65)%w:
        print(it, len(Q))
        y.append(len(Q))
        x.append(it)
    Q = {i for i in q if cmod(i) in G} # Plausible locations

a,b,c = polyfit(x, y, deg=2) # 605492675373143
print(int(polyval((a,b,c), [64, w, 2*w, 3*w, 26501365][-1]))+1)