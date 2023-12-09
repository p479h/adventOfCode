import itertools as it
from functools import cache

def part1(p):
    pts = [0, 0]
    for i in range(1000):
        player = i // 3 % 2 # 0 1 0 1...
        p[player] = (p[player] + (i%100+1) -1 ) % 10 + 1
        if (i+1) % 3 == 0:
            pts[player] += p[player]
            if pts[player] >= 1000:
                pts_loser = pts[not player]
                return i, pts, pts_loser


# Variation of answer from reddit 
@cache
def part2(p1, s1, p2, s2):
    w1 = w2 = 0
    # Note that here we allow for three identical throws 1's!
    # This was not clear from the question :(
    for dice in map(sum,it.product(*(range(1, 4),)*3)):
        p1_copy = (p1 + dice)%10 or 10
        s1_copy = s1 + p1_copy
        if s1_copy >= 21:
            w1 += 1
        else:
            w2_copy, w1_copy = part2(p2, s2, p1_copy, s1_copy)
            w1 += w1_copy
            w2 += w2_copy
    return w1, w2

def main():
    test = 4, 8
    data = 4, 5
    
    # PArt 1
    p = list(data)
    i, pts, pts_loser = part1(list(p))
    print(pts_loser*(1+i))

    # Part 2
    print(part2(p[0], 0, p[1], 0))


if __name__ == "__main__":
    main()