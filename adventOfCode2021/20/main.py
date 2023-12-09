
import itertools as it

def extend(m):
    n = 4
    w =len(m[0])
    top = [["0" for _ in range(w+n*2)] for _ in range(n)]
    bot = [["0" for _ in range(w+n*2)] for _ in range(n)]
    return  top + [[*("0"*n), *r, *("0"*n)] for r in m] + bot

def main():
    ag, im = open("./data.txt").read().replace("#", "1").replace(".","0").split("\n\n")
    im = [list(l) for l in im.split("\n")]
    for _ in range(50):
        if _ % 2 == 0: # To account for edges
            im = extend(im)
        # Since the image and output swap, we must extend both
        w, h = len(im[0]), len(im)
        im = [[ag[int("".join([im[k][l] if (0<=k<h and 0<=l<w) else "0" for k,l in it.product(range(i-1,i+2),range(j-1,j+2))]),base=2)] for j in range(w)][1:-1] for i in range(h)][1:-1]
    out = [list(map(int,l)) for l in im]
    print("\n".join(["".join([".#"[c] for c in r]) for r in out]))
    print(sum(it.chain(*out)), sep="\n") # 5425 is the right answer?


if __name__ == "__main__":
    main()