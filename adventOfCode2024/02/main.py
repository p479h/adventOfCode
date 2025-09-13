import re 
import itertools as it

def main():
    reports = [list(map(int, l.split())) for l in open("./data.txt")]
    is_safe = lambda r: all((b-a)*(r[1]-r[0])>0 and abs(b-a) in (1,2,3) for a,b in it.pairwise(r))
    without_one = lambda r: (r[:i]+r[i+1:] for i in range(len(r)))
    safe1 = sum(map(is_safe,reports))
    safe2 = sum(any(map(is_safe,without_one(r))) for r in reports)
    print(safe1, safe2) 
    return 0 

if __name__ == "__main__":
    main()
