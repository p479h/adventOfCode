from functools import partial 

def main():
    data = tuple(tuple(map(int, l.split())) for l in open("./data.txt"))
    # Part 1 and 2
    def f(part, l):
        if not any(l): # All l are 0
            return l[0]
        if part == 1:
            return l[-1] + f(part, [a-b for a,b in zip(l[1:], l[:-1])])
        # Part 2
        return l[0] - f(part, [a-b for a,b in zip(l[1:], l[:-1])])
    print(sum(map(partial(f, 1), data))) # Part 1
    print(sum(map(partial(f, 2), data))) # Part 2
    return 0

if __name__ == "__main__":
    main()
