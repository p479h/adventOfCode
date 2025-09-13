from itertools import chain
from collections import deque

def toi(n: complex) -> tuple[int]: # Number to index
    return (round(n.real), round(n.imag))

def ton(i: tuple[int]) -> complex: # Index to number
    return complex(*i)

def neighbors(s: complex, data: dict, h: int, w: int) -> deque[tuple]:
    # Returns neighbors of the same type
    nbs = deque([],4)
    for d in (1,-1,1j,-1j):
        (i,j) = toi(ton(s)+d)
        if (0<=i<h and 0<=j<w) and data[(i,j)]==data[s]:
            nbs.append((i,j))
    return nbs

    

def find_regions(data: dict[tuple,str], pool: deque[tuple]) -> None:
    """
    Finds the entire region by picking neighbors in pools.
    """ 
    # Dimensions of garden
    h, w = map(max, zip(*data)) # Note this is h-1, w-1

    sector = deque([])
    while pool:
        # Getting space for group
        group = set()

        # Getting a random starting point from 
        Q = deque([pool[0]])

        # Going around while there are still neighbors
        while Q:
            nbs=neighbors(s:=Q.popleft(), data, h+1, w+1)
            group.add((s,len(nbs))) # Group contains position and number of neighbors for the perimeter calculation
            pool.remove(s)
            # Adding elements that have not been searched to the queue
            for nbi in nbs:
                if nbi in pool and not (nbi in Q):
                    Q.append(nbi) # nbs will be searched next

        # At the end fo the loop, every neighbor has been found and is contained in group
        sector.append(group)
    return sector
                

def main():
    # Getting all characters and their indices
    data = {
        (i,j): c 
        for i,r in enumerate(open('./test.txt'))
        for j,c in enumerate(r.strip())
    }

    # Values that have not been searched yet
    pools = {
        k: deque([
            ij
            for ij, c in data.items() 
            if c == k
        ])
        for k in set(data.values())
    }

    # Sectors that are found for each pool
    sectors = {
        c: find_regions(data, pool)
        for c,pool in pools.items()
    }

    prices = {
        k: [
            len(sector)*sum(
                4-n 
                for _,n in sector
            )
            for sector in groups
        ]
        for k, groups in sectors.items()
    }
    # Part 1
    print(sum(chain(*prices.values())))

    # Part 2
    import numpy as np
    from scipy.ndimage import label
    import matplotlib.pyplot as plt 
    from scipy.signal import convolve2d
    d = np.array([list(l.strip()) for l in open('test.txt')])
    plt.imshow(
        convolve2d(
            label(d=='I')[0]==2,
            [[-1,1],[1,-1]]
        )
    )
    plt.figure()
    plt.imshow(
            label(d=='I')[0]==2
    )
    plt.show()


if __name__ == '__main__':
    main()