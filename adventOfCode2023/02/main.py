import re 

def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def main():
    test_path = "./test.txt"
    data_path = "./data.txt"
    data = read([test_path, data_path][1]).split("\n")

    # Part 1
    limits = {"blue": 14, "red": 12, "green": 13}.values()
    def game(s): 
        game_id = re.search(r"\d+(?=:)", s).group(0)
        max_amounts = {"blue": 0, "red": 0, "green": 0}
        for amount, color in re.findall(r"(\d+) (\w+)", s):
            max_amounts[color] = max(int(amount), max_amounts[color])
        return game_id, tuple(max_amounts.values())
    total = 0
    power = 0
    for gid, am in map(game, data):
        if all(x<=v for v,x in zip(limits, am)):
            total += int(gid)
        # Part 2
        power += am[0]*am[1]*am[2]
    print(total, power)
    return 0

if __name__ == "__main__":
    main()
