import re 
from pathlib import Path

data_path = Path('./data')
test_data_path = data_path/'test_data.txt'
real_data_path = data_path/'data.txt'

def load_lines(path):
    with open(path) as f:
        l = (l for l in f.readlines() if l.strip())
    return l

def check_policy(s):
    pat = r"(\d+)-(\d+) (\w): (\w+)"
    groups = re.match(pat, s)
    lb, ub = int(groups.group(1)), int(groups.group(2))
    letter = groups.group(3)
    password = groups.group(4)
    return lb <= password.count(letter) <= ub

def check_policy2(s):
    pat = r"(\d+)-(\d+) (\w): (\w+)"
    groups = re.match(pat, s)
    lb, ub = int(groups.group(1))-1, int(groups.group(2))-1
    letter = groups.group(3)
    password = groups.group(4)
    p1 = letter == password[lb]
    p2 = letter == password[ub]
    return p1 and not p2 or p2 and not p1

def main():
    lines = load_lines(real_data_path)
    total = sum(map(check_policy2, lines))
    print(total)

if __name__ == "__main__":
    main()
