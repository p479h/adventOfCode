from collections import deque
from itertools import product

toi = lambda i: (round(i.real), round(i.imag))
def search_9(data,s):
    h, w = map(len,(data,data[0]))
    data = list(map(list,data))
    D = {(i,j): int(c) for i,l in enumerate(data) for j,c in enumerate(l)}
    Q = deque([s])
    seen = set()
    while Q:
        i = Q.popleft()
        seen |= {toi(i)}
        for d in (1,-1,1j,-1j):
            n = toi(i+d)
            if 0<=n[0]<h and 0<=n[1]<w and (D[n]-D[toi(i)]==1) and n not in seen:
                Q.append(i+d)
    return len([(i,j) for i,j in seen if data[i][j] == '9'])

def search_all_routes(data,s,w=None,h=None,D=None,seen=None):
    if seen is None:
        seen = set()
        h, w = map(len,(data,data[0]))
        D = {(i,j): int(c) for i,l in enumerate(data) for j,c in enumerate(l)}
    i = toi(s)
    seen.add(i)
    for d in (1,-1,1j,-1j):
        n = toi(s+d)
        if 0<=n[0]<h and 0<=n[1]<w and (D[n]-D[i]==1) and n not in seen:
            if D[n] == 9:
                yield 1
            else:
                yield from search_all_routes(data,s+d,w,h,D,seen)
    seen.remove(i)

def search(data,pt=1):
    rh,rw = map(range, map(len,(data,data[0])))
    for s in (complex(i,j) for i,j in product(rh,rw) if data[i][j]=='0'):
        if pt == 1:
            yield search_9(data,s)
        else:
            yield from search_all_routes(data,s)

def main():
    # Collecting the data 
    data = [l.strip() for l in open("./data.txt")]
    for pt in (1,2):
        print('Pt %i:'%pt, sum(search(data, pt))) # 794 YAY
    return 0

if __name__ == "__main__":
    main()
