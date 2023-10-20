import numpy as np
from pathlib import Path
from scipy.signal import fftconvolve as convolve
from itertools import product 

data_path = Path('./data')
test_data_path = data_path/'test_data.txt'
real_data_path = data_path/'data.txt'

# convolution filter (Sums around)
mat = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])

# keys representing the number of people in each place
keys = {"#": 1, ".": 0, "L": -1}
keys_rev = {v:k for k,v in keys.items()}

def load_data(path: str):
    with open(path) as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
        table = [list(map(keys.get, chars)) for chars in lines]
        return np.array(table)

def count_seats1(table: np.ndarray[int]):
    s = convolve(table==keys["#"], mat, "same").round(0).astype(int)
    return s

def count_seats2(t: np.ndarray):
    # Returns the accessible chairs for each ij
    # n[i][j] has shape [8, *, 2]
    Ni,Nj = t.shape
    directions = np.array(
        [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
    )

    # Storing memory for the seat counts 
    s = np.zeros_like(t)
    for i,j in product(range(Ni), range(Nj)):
        for d in directions:
            ni,nj = d[0]+i, d[1]+j
            while 0<=ni<Ni and 0<=nj<Nj:
                if t[ni,nj] == keys["#"]:
                    s[i,j] += 1
                    break
                elif t[ni,nj] == keys["L"]:
                    break
                ni += d[0]
                nj += d[1]
    return s
    
    
def evolve(t: np.ndarray, seat_function: callable = count_seats1, tol: int = 4):
    # t: table re: real, im: imaginary
    # Real 1 is free, Im 1 is occupied, 0 is floor
    s = seat_function(t)

    # Floor
    floor = t == 0

    # Must get up
    up = (s >= tol) & (~floor)

    # Must sit
    sit = ~floor & (s == 0)
    
    t[floor] = keys["."]
    t[up] = keys["L"]
    t[sit] = keys["#"]

def print_table(t: np.ndarray):
    intfy = lambda t: tuple(map(int,t))
    for row in t:
        for char in map(keys_rev.get, intfy(row)):
            print(char, sep = "", end="")
        print()
    

def main():
    path = [test_data_path, real_data_path][1]
    table = load_data(path)
    # Part 1
    copy = table.copy()+1
    while np.sum(np.abs(copy-table)) > 0:
        #print_table(table)
        copy = table.copy()
        evolve(table, count_seats1, 4)
    print((table==1).sum())

    # Part 2
    table = load_data(path)
    copy = table.copy()+1
    while np.sum(np.abs(copy-table)) > 0:
        copy = table.copy()
        evolve(table, count_seats2, 5)
    print((table==1).sum())
    
    return 0

if __name__ == "__main__":
    main()
    
