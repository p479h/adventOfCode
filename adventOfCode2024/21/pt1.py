from heapq import heappop, heappush, heapify
from collections import deque 

def ijs(h, w):
    yield from ((i,j) for i in range(h) for j in range(w))

def nbs(i,j):
    return ((i-1, j),(i+1,j), (i,j-1),(i,j+1))

def print_map(garden, dist):
    for i,r in enumerate(garden):
        for j,c in enumerate(r):
            if not (i,j) in dist:
                print(c,end="")
            else:
                print(c if c == "#" else dist[i,j]%10 if dist[i,j] < 1e9 else c, end="")
        print()

def build_dists(garden, h, w, nsteps, S):
    # Building seeminly possible paths in a fast way
    si, sj = S
    dist = {(i,j): sum(map(abs,(i-si,j-sj))) for i,j in ijs(h,w) if sum(map(abs,(i-si,j-sj)))<=nsteps and garden[i][j]!="#"}
    bad = {}
    while True:
        for (i,j),v in dist.items():
            if v == 0:
                continue 
            # Looking for neighbours with plausible path
            nb = [dist[ni,nj] for ni,nj in nbs(i,j) if (ni,nj) in dist and dist[ni,nj]<=v]
            # Removing element that does not have neighbours and looking again
            if not nb: # No neighbours 
                bad[i,j] = "?"
                del dist[i,j]
                break
        else: 
            break
    return dist, bad
    
    
def main():
    garden = tuple(map(list, open("data.txt").read().splitlines()))
    h, w = map(len, (garden, garden[0]))
    S = [(i,j) for i,r in enumerate(garden) for j,c in enumerate(r) if c == "S"][0]
    si, sj = S
    nsteps = 64
    dist, empty = build_dists(garden, h, w, nsteps, S) # Distance and inconclusive
    seen = set(dist) # All numbered elements count as seen 
    Q = [(sum(map(abs,(ij[0]-si,ij[1]-sj))),ij) for ij in dist if any(nb in empty for nb in nbs(*ij))]
    while Q:
        d, ij = _,(i,j) = heappop(Q)
        seen.add(ij)
        if d>nsteps:
            continue
        for nb in (nb for nb in nbs(i,j) if nb in empty or nb in Q): # Looping over neighbours in holes
            if not nb in seen:
                heappush(Q, (d+1, nb))
            dist[nb] = min(d+1, dist[ij]+1)
    
    np = sum(v%2==0 for v in dist.values())
    print(np)
    print_map(garden, dist)

    return 0

if __name__ == "__main__":
    main()
