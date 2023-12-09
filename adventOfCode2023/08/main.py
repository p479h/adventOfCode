import re 
from math import gcd, prod
from functools import reduce 

def main():
    path = ["./test.txt", "./data.txt"]
    LR, MAP = open(path[1]).read().split("\n\n")
    LR = tuple(map("LR".index,LR))
    N = len(LR)
    MAP = dict((k,(*v,)) for k, *v in re.findall(r"(\w{3}) = \((\w{3}), (\w{3})\)", MAP))
    # Part 1
    P, i = "AAA", -1
    while P != "ZZZ":
        P = MAP[P][LR[(i:=(i+1))%N]]
    print("Solution part 1:",i)
    
    # Part 2
    Ps, i = [s for s in MAP if s.endswith("A")], 0
    steps = [0 for _ in Ps]
    while not all(p.endswith("Z") for p in Ps):
        Ps = [MAP[p][LR[(s or i)%N]] if not p.endswith("Z") else p for s,p in zip(steps,Ps)]
        i += 1
        steps = [i if not s and p.endswith("Z") else s for s, p in zip(steps, Ps)]
        #print(Ps, steps, [s%N for s in steps])
    print("Greatest common divisor:",cd:=reduce(gcd, steps))
    print("Number of GCD:", cds:=[s//cd for s in steps]) # ALL ARE PRIMES! So they can't share common factors except for the greatest common divisor
    print("Product of numebr of GCDs (including the COMMON ONE!):", prod(cds)*cd)
    return 0 

if __name__ == "__main__":
    main()
