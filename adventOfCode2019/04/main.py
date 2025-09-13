import numpy as np
from pathlib import Path

def part1(n1, n2):
    is_good = lambda n: n == "".join(sorted(n)) and len(set(n)) < len(n)
    return sum(is_good(n) for n in map(str, range(n1, n2+1)))

def part2(n1, n2):
    is_good = lambda n: n == "".join(sorted(n)) and len(set(n)) < len(n) and 2 in map(n.count, n)
    return sum(is_good(n) for n in map(str, range(n1, n2+1)))
    

def main():

    n1, n2 = 152085, 670283
    # Part 1
    answer1 = part1(n1, n2)
    print("Answer to part 1 is %i"%answer1)

    # Part 1
    answer2 = part2(n1, n2) # 135 is too low
    print("Answer to part 1 is %i"%answer2)


if __name__ == "__main__":
    main()
