import re 
import random
from itertools import pairwise

def sort(rules, ordering):
    ordering = list(ordering)
    new_ordering = []
    while ordering:
        min_ = next((b for b in ordering
             if not any((b,a) in rules for a in ordering)))
        
        new_ordering.append(
            ordering.pop(ordering.index(min_))
        )
    return new_ordering[::-1]
        


def main():
    r,o = open("./data.txt").read().split("\n\n")
    rules = re.findall(r"(\d+)\|(\d+)", r)
    orderings = [tuple(l.split(',')) for l in o.splitlines()]

    # Part 1
    valid = set(o for o in orderings if not any(r[::-1] in rules for r in pairwise(o)))
    midsum = lambda ords: sum(map(int, (o[len(o)//2] for o in ords)))
    print(midsum(valid))

    # Part 2
    invalid = set(orderings)-valid
    corrected = list(sort(rules, o) for o in invalid)
    print(midsum(corrected))
    
    
    return 0

if __name__ == "__main__":
    main()
