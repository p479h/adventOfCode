from collections import Counter, deque
from itertools import combinations,chain


def rule(n):
    if n==0:
        return 1
    elif (N:=len(str(n)))%2==0:
        return [n//10**(N//2),n%10**(N//2)]
    return n*2024

def apply_rule(l):
    for i,(n,e) in enumerate(l):
        if isinstance(e,int):
            l[i] = (n,rule(e))
        else:
            apply_rule(e)

def optimize(l):
    counts = Counter()
    for (n,*E) in l:
        for e in (E[0] if isinstance(E[0],list) else E):
            counts[e]+=n
    l.clear()
    l.extend([(n,e) for e,n in counts.items()])

def main():
    data = list(map(int,next(open("./data.txt")).split()))
    data = deque([[1,n] for n in data])
    for _ in range(75):
        apply_rule(data)
        optimize(data)
        if (_+1)%25==0:
            print(_+1,sum(n for n,_ in data))
        
    return 0

if __name__ == "__main__":
    main()
