import re 

def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def main():
    test_path = "./test.txt"
    data_path = "./data.txt"
    data = read([test_path, data_path][1]).splitlines()
    # Part 1 
    digits = [list(filter(str.isnumeric, line)) for line in data]
    print(sum([int(d[0]+d[-1]) for d in digits]))

    # Part 2 (SINGLE DIGITS COUNT TWICE!!!! "one"-> "11")
    replacements = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", *"123456789"]
    word_to_num = {d: str(i%9+1) for i, d in enumerate(replacements)}
    digits = [list(map(word_to_num.get, re.findall(rf"(?=({'|'.join(replacements)}))", line))) for line in data]
    print(sum([int(d[0]+d[-1]) for d in digits]))
    return 0

if __name__ == "__main__":
    main()
