from itertools import combinations 

def main():
    data = open("./data.txt").read().splitlines()
    rows = [int(not "#" in r)*(1e6-1) for r in data]
    cols = [int(not "#" in c)*(1e6-1) for c in zip(*data)]
    pos = [(i+sum(rows[:i]),j+sum(cols[:j])) for i,r in enumerate(data) for j,c in enumerate(r) if c == "#"]
    diff = sum(abs(ai-bi)+abs(aj-bj) for (ai,aj),(bi,bj) in combinations(pos,2))
    print(diff) # 10165598, 678729486878.0 is too high
    return 0

if __name__ == "__main__":
    main()
