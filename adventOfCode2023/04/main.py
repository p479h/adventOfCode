import re 
from collections import defaultdict

def main():
    s = 0
    matches = defaultdict(lambda: 1)
    for li, line in enumerate(map(str.strip, open("./data.txt"))):
        l1, l2 = tuple(map(lambda l: set(map(int,l.split())), re.findall(r"([\d ]{5,})", line)))
        n_matches = len(l1&l2)
        s += bool(n_matches)*2**(n_matches-1)
        matches[li] += 0 # Ensure that this index exists
        for i in range(1,n_matches+1):
            matches[i+li] += matches[li]
    print(s)
    print(sum(matches.values()))
    return 0

if __name__ == "__main__":
    main()
