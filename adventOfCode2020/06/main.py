from functools import reduce
from operator import and_
from pathlib import Path

data_path = Path('./data')
test_data_path = data_path/'test_data.txt'
real_data_path = data_path/'data.txt'

def load_data(path):
    with open(path) as f:
        groups = [g.split("\n") for g in f.read().split("\n\n")]
        return groups

def count_answers(groups):
    unique = (set(a for s in g for a in s) for g in groups)
    return sum(len(list(u)) for u in unique)

def count_common_answers(groups):
    unique = (reduce(and_, [set(p) for p in g]) for g in groups)
    return sum(len(list(u)) for u in unique)

def main():
    groups = load_data(test_data_path)
    count = count_answers(groups)
    common_count = count_common_answers(groups)
    print("Individual answers", count)
    print("Common answers", common_count)


if __name__ == "__main__":
    main()
