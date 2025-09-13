import re 
from operator import mul
from itertools import starmap

D1 = {"U":(-1,0),"L":(0,-1),"D":(1,0),"R":(0,1)}
D2 = ((0,1), (1,0), (0,-1), (-1,0))
def main():
    # Strategy: 
    # 1. Use green's theorem to compute the inner area.
    #    This will leave out the outer edges of the perimeter
    # 2. Account for the outer edges of the perimeter by:
    #   2.1 Adding 3/4 * n_{outward corners} old x new @ z_hat > 0
    #   2.2 Adding 1/4 * n_{inward corners}  old x new @ z_hat < 0
    #   2.3 Adding 1/2 * n_{non corners}
    A = [2,2] # 3/2 because initial corner is never accounted for, 1/2... I don't know...
    xs, os = [[0,0],[0,0]], [[0,0],[0,0]]
    for d in (re.findall(r"(\w) (\d+) \(#([\d\w]{5})([\d\w])\)", l)[0] for l in open("./data.txt")):
        ns = [tuple(starmap(mul, zip(D1[d[0]], [int(d[1])]*2))), # Computing vector n
              tuple(starmap(mul, zip(D2[int(d[3])], [int(d[2], base=16)]*2)))]
        for i, ((y,x),n,o) in enumerate(zip(xs, ns, os)):
            A[i] += 1/2*(-y*n[1] + x*n[0]) + (abs(sum(n))-1)/2 + (3 if o[0]*n[1]-o[1]*n[0] > 0 else 1)/4
            xs[i][0], xs[i][1], os[i] = y + n[0], x + n[1], n
    print("Solution part 1: %i\nSolution part 2: %i"%tuple(map(int,A)))
    return 0

if __name__ == "__main__":
    main()