import re 


def main():
    test_data = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    data = open("./data.txt").read()

    #data = data
    pairs = [tuple(map(int,pair)) for pair in re.findall(r'mul\((\d+),(\d+)\)',data)]
    pt1 = sum(a*b for a,b in pairs)

    # Part 2
    pt2 = 0
    matches = iter(re.findall(r'mul\((\d+),(\d+)\)|(do\(\))|(don\'t\(\))',data))
    for p in matches:
        if p[-1]:
            while not p[-2]:
                p = next(matches)
        while p[-2]:
            p = next(matches)
        pt2 += int(p[0])*int(p[1])
    print(pt1, pt2) # 166357705 88811886
    return 0

# Def main im
def main2():
    # Reddit inspired
    pt1,pt2,active = 0,0,True
    for a,b,do,dont in re.findall(r'mul\((\d+),(\d+)\)|(do\(\))|(don\'t\(\))',open("./data.txt").read()):
        active = bool(do) if (dont or do) else active
        if not (do or dont):
            pt1 += int(a)*int(b)
            pt2 += int(a)*int(b)*active
    print(pt1,pt2)

if __name__ == "__main__":
    main()
    main2()
