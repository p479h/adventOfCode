from itertools import combinations 

def main():
    m = 2 #1 for part 1 or 1e6 for part 2
    data = open("./data.txt").read().splitlines()
    rows = [(not "#" in r)*(m-1) for r in data]
    cols = [(not "#" in c)*(m-1) for c in zip(*data)]
    pos = [(i+sum(rows[:i]),j+sum(cols[:j])) for i,r in enumerate(data) for j,c in enumerate(r) if c == "#"]
    diff = sum(abs(ai-bi)+abs(aj-bj) for (ai,aj),(bi,bj) in combinations(pos,2))
    print(diff) # 10165598, 678729486878 is too high
    return 0

if __name__ == "__main__":
    main()
