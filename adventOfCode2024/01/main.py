def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def main():
    test_path = "./test.txt"
    data_path = "./data.txt"
    # Part 1 
    A,B = zip(*(map(int,pair.split()) for pair in open(data_path)))
    ans1 = sum(abs(b-a) for a,b in zip(*map(sorted,[A,B])) )
    ans2 = sum(b*A.count(b) for b in B)
    print(ans2)
    return 0

if __name__ == "__main__":
    main()
