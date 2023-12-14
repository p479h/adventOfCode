from collections import defaultdict
from copy import deepcopy as dp

def R(t): # Rotates 90 deg clockwise
    return [list(r[::-1]) for r in zip(*t)]

def fall_up(t):
    for (i,j) in ((i,j) for i,r in enumerate(t) for j,c in enumerate(r) if c=="O"):
        while (i > 0) and t[i-1][j] == ".":
            t[i-1][j], t[i][j], i = "O", ".", i-1
    return t

def cycle(t):
    for _ in range(4):
        t[:] = R(fall_up(t))
    return t

def main():
    data = list(map(list,open("./data.txt").read().splitlines()))
    # Part 1
    s = sum(len(data)-i for i,r in enumerate(fall_up(dp(data))) for j,c in enumerate(r) if c == "O")
    print("Part 1 solution: %i"%s)
    
    # Part 2 
    # Experimentation said 34 is the space between the same values with 137th iteration having 9600
    # (1000000000-137)%34 -> 23, so 23 indices above 9600's.
    # Iteration 137 + 23 = 160th iteration with i=159 -> 90551 which is the right answer for this input
    # Based on this known answer the algorithm below was created (but only tested on this input)
    # Finding the repeats
    loads = defaultdict(lambda : [])
    for i in range(300):
        data = cycle(data)
        if i%2==0: # Avoids repeating numbers
            loads[sum(len(data)-i for i,r in enumerate(data) for j,c in enumerate(r) if c == "O")].append(i)
            v, js = max(loads.items(), key=lambda e: len(e[1]))
            if len(js) > 2:
                break
    else:
        raise Exception("Repeating pattern not found")
    # Last few cycles 
    for _ in range((1000000000-js[-1])%(js[-1] - js[-2])):
        data = cycle(data)
        v = sum(len(data)-i for i,r in enumerate(data) for j,c in enumerate(r) if c == "O")
    print("Part 2 solution: %i"%v)

    return 0

if __name__ == "__main__":
    main()
