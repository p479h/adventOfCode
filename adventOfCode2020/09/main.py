from pathlib import Path
from itertools import combinations

data_path = Path('./data')
test_data_path = data_path/'test_data.txt'
real_data_path = data_path/'data.txt'


def load_data(path):
    with open(path) as f:
        lines = (l.strip() for l in f.readlines() if l.strip())
    return tuple(map(int, lines))


def check_preamble(data, index, window=5):
    lb = max(0, index - window)
    ub = index
    for (a,b) in combinations(data[lb:ub], 2):
        if a + b == data[index]:
            return True
    return False

def find_problematic_numbers(data, window = 5):
    bad = []
    for i, num in enumerate(data[window:], start=window):
        good_preamble = check_preamble(data, i, window)
        if not good_preamble:
            bad.append((i, num))
    return bad

def find_weakness(data, window):
    index, number = find_problematic_numbers(data, window)[0]

    # The number can't include the actual number
    ub = data.index(number)

    # The number can be up to n*window back
    lb = 0

    # Looping over the combinations of indices between lb and ub
    for l, u in combinations(range(lb, ub), 2):
        if sum(data[l:u]) == number:
            return l, u
    

def main():
    path, window = [(real_data_path, 25),(test_data_path, 5)][0]
    data = load_data(path)
    bad = find_problematic_numbers(data, window)
    print(bad)
    lb, ub = find_weakness(data, window)
    cont = data[lb:ub]
    print(cont, sum(cont))
    print(min(cont) + max(cont))

if __name__ == "__main__":
    main()
    
