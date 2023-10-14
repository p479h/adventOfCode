from pathlib import Path
from math import ceil
from functools import reduce
from operator import mul

data_path = Path('./data')
test_data_path = data_path/'test_data.txt'
real_data_path = data_path/'data.txt'

def load_map(path):
    with open(path) as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    return lines

def gen_indices(map_, slope):
    dy, dx = slope
    h, w = len(map_), len(map_[0])

    n_indices = int(round(h/dy,0))
    i = range(0, h, dy)
    j = range(0, ceil(h/dy) * dx, dx)
    j = map(lambda J: J%w, j)
    return i,j

def count_trees(map_, slope):
    is_tree = lambda i,j: map_[i][j]=="#"
    i, j = gen_indices(map_, slope)
    return sum(is_tree(I,J) for I,J in zip(i,j))


def main():
    map_ = load_map(real_data_path)
    totals = []
    slopes = [(1, 1),(1, 3), (1, 5), (1, 7), (2, 1)]
    for slope in slopes:
        n_trees = count_trees(map_, slope)
        totals.append(n_trees)

    prod = reduce(mul, totals)
    print(totals)
    print("Number of trees is %i"%prod)

if __name__ == "__main__":
    main()
