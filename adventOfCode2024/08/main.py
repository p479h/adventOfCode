from itertools import groupby, chain, combinations


def main():
    p2i = lambda p: (round(p.real),round(p.imag))
    i2p = lambda i,j: complex(i,j)
    grouper = lambda e: e[0]
    grid = [l.strip() for l in open('./data.txt')]
    h,w = map(len,(grid,grid[0]))
    antenas =((f, i2p(i,j)) for i,l in enumerate(grid) for j,f in enumerate(l) if f!='.')
    grouped = sorted(antenas, key=grouper) # Neighbours are art of the same grou
    groups = tuple(tuple(v) for g,v in groupby(grouped, key=grouper)) # Same frequency

    for part in (1,2):
        antenodes = chain( *(map(p2i,chain(*[[A+(A-B)*n,B+(B-A)*n] for n in range(part!=2,[max(h,w),2][part!=2])]))
                             for g in groups for (_,A),(_,B) in combinations(g,2)) )
        inner_antenodes = [(i,j) for (i,j) in set(antenodes) if 0<=i<h and 0<=j<w]
        print('Pt %i: %i'%(part,len(inner_antenodes))) # 369, 1169
    return 0 

if __name__ == "__main__":
    main()
