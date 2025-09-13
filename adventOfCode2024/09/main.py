from itertools import chain, filterfalse, groupby

def fragment(mem, pt=1):
    mem = list(mem) # Copy
    mem_back = reversed([(i,v) for i,v in enumerate(mem) if v!=-1])
    if pt==1:
        for a in (i for i,v in enumerate(mem) if v==-1):
            i,v = next(mem_back)
            if i>a: # Beyond this point, all addresses are -1
                mem[a], mem[i] = v, -1 
                continue
            return mem[:a]
    elif pt == 2:
        grps = ((g,tuple(v)) for g,v in groupby(enumerate(mem), key=lambda e: e[1]))
        fi_groups = [list(next(zip(*v))) for g,v in grps if g==-1] # Groups of empty indices
        for g, vals in groupby(mem_back, lambda e: e[1]): # Looping over memory values and indices starting from the back
            indices = next(zip(*vals))
            lb, ub = min(indices), max(indices)+1
            n = ub-lb
            for fi_grp in filter(bool, fi_groups): 
                if min(fi_grp) > lb:
                    break
                if len(fi_grp) >= n:
                    for i in range(n):
                        mem[fi_grp.pop(0)], mem[lb+i] = g, -1
                    break
        return mem
    raise ValueError()

def main():
    data = map(int,open('./data.txt').read())
    mem = list(chain(*(([i//2,-1][i%2],)*n  for i, n in enumerate(data))))
    test = lambda l: sum(i*v for i,v in enumerate(l) if v!=-1) 
    print('Pt 1', test(fragment(mem,1)))
    print('Pt 2', test(fragment(mem,2))) # 6382582136592 just right
                 
    
    return 0

if __name__ == "__main__":
    main()
