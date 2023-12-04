from re import finditer as find
from functools import reduce 
from math import prod
from collections import deque 
from itertools import product

# Note: This code was adapted to avoid look-ups in more than 3 lines at a time
# For this reason it is impossible to read

def main():
    test_path = "./test.txt"
    data_path = "./data.txt"
    path = [test_path, data_path][1]

    lines = open(path).readlines()
    s = 0
    all_chars = []
    chars = deque([{(i,m.start(0)): [] for m in find(r"[^.\d\n]", lines[0])}],3)
    all_chars.append(chars[0])
    for i,line in enumerate(lines):
        if i < len(lines)-1: # Adding it every row to save on computation time on the searching step
            chars.append({(i+1,m.start(0)): [] for m in find(r"[^.\d\n]", lines[i+1])})
            all_chars.append(chars[-1])
        for n in find(r"\d+", line):
            box = set(product((i-1,i,i+1), range(n.start()-1, n.end()+1)))
            if loc := box & {p for l in chars for p in l}:
                s += int(n.group())
                for pos in loc: 
                    for dictionary in chars:
                        if pos in dictionary:
                            dictionary[pos].append(int(n.group()))

    print(s) # 539713 (Correct answer)
    s2 = sum(prod(list_) for dict_ in all_chars for list_ in dict_.values() if len(list_) == 2)
    print(s2) # 84159075 (Correct answer)
    return 0

if __name__ == "__main__":
    main()
