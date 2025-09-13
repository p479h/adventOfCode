from re import findall
from functools import reduce
from itertools import product
from operator import add, mul

def main():
    path = "./data.txt"
    run = lambda ops: sum(t 
            for t,*n in (map(int,findall(r'(\d+)',l)) for l in open(path))
                if t in (reduce(lambda tot,no: no[1](tot,no[0]),zip(n[1:], oc), n[0])
                            for oc in product(ops, repeat=len(n)-1))
    )
    # Removing repeating sequences
    # Pt1:  4364915411363
    # Pt2: 38322057216320
    print('Pt1: %i'%run((add,mul)))
    print('Pt2: %i'%run((add,mul,lambda a,b: a*10**next(i for i in range(20) if b//10**i==0)+b)))
    return 0                                        

if __name__ == "__main__":
    main()
