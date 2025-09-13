import numpy as np
from pathlib import Path

def part1(n):
    return n//3-2

def part2(ns):
    total = 0
    for n in ns:
        n = part1(n)
        while n>0:
            total += n
            n = part1(n)
    return total

def main():
    data_path = Path(__file__).parent/"data.txt"
    test_data_path = Path(__file__).parent/"test_data.txt"
    data = np.loadtxt(data_path)
    test_data = np.loadtxt(test_data_path)
    
    # Part 1
    answer1 = np.sum(part1(data))
    print("Answer to part 1 is %i"%answer1)

    # Part 1
    answer2 = part2(data)
    print("Answer to part 1 is %i"%answer2)


if __name__ == "__main__":
    main()
