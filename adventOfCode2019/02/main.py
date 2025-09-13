import numpy as np
from pathlib import Path

def part1(n):
    for i in range(len(n)//4):
        print(i*4, n[4*i])
        program = n[4*i]
        i1 = n[4*i+1]
        i2 = n[4*i+2]
        i3 = n[4*i+3]
        match program:
            case 1:
                n[i3] = n[i1]+n[i2]
            case 2:
                n[i3] = n[i1]*n[i2]
            case 99:
                break
    return n[0]

def part2(ns):
    for i in range(1, 100):
        for j in range(1, 100):
            ns_copy = [ns[0], i, j, *ns[3:]]
            if part1(ns_copy) == 19690720:
                return i,j, 100*i+j
    else:
        print("NO answer found for part 2")

def main():
    data_path = Path(__file__).parent/"data.txt"
    test_data_path = Path(__file__).parent/"test_data.txt"
    data = np.loadtxt(data_path, dtype=int, delimiter=",")
    test_data = np.loadtxt(test_data_path, dtype=int, delimiter=",")
    
    # Part 1
    answer1 = part1([data[0], 12, 2, *data[3:]])
    print("Answer to part 1 is %i"%answer1)

    # Part 1
    #answer2 = part2(data)
    #print("Answer to part 2 is %i,%i, such that 100*noun + verb = %i"%answer2)


if __name__ == "__main__":
    main()
