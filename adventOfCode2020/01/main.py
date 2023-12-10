from pathlib import Path
from operator import mul
from functools import reduce
from itertools import combinations


data_path = Path('./data')
test_data_path = data_path/'test_data.txt'
real_data_path = data_path/'data.txt'

def load_numbers(path):
    with open(path) as f:
        lines = f.readlines()
        lines = [l for l in lines if l.strip()]
    numbers = list(map(int, lines))
    return numbers

# Checking which combination is higher equal to target
def find_prod_of_target_sum(numbers, target, n_entries = 2):
    for vals in combinations(numbers, n_entries):
        if sum(vals) == target:
            return reduce(mul, vals)


if __name__ == "__main__":
    # Loading the numbers
    numbers = load_numbers(real_data_path)
    target = 2020

    prod = find_prod_of_target_sum(numbers, target, 3)
    print(prod)
