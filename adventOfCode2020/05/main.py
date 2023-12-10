from pathlib import Path

data_path = Path('./data')
test_data_path = data_path/'test_data.txt'
real_data_path = data_path/'data.txt'

codes = {
    "F": 0,
    "B": 1,
    "L": 0,
    "R": 1
}

def load_sets(path):
    with open(path) as f:
        return [f.strip() for f in f.readlines() if f.strip()]

def code_to_bin(code):
    return "".join(list(str(s) for s in map(codes.get, code)))

def bin_to_rowcol(bin_):
    row = int(bin_[:7],base=2)
    col = int(bin_[7:],base=2)
    return row, col

def code_to_rowcol(code):
    return bin_to_rowcol(code_to_bin(code))

def code_to_id(code):
    row, col = code_to_rowcol(code)
    return 8*row + col

def find_seat(codes):
    ids = [(i,j) for i in range(10,116) for j in range(8)]
    for code in codes:
        row,col = code_to_rowcol(code)
        ids.pop(ids.index((row,col)))
    return ids

def main():
    codes = load_sets(real_data_path)
    largest = max(map(code_to_id, codes))
    print(largest)
    seats = find_seat(codes)
    row, col = seats.pop(0)
    id_ = row*8 + col
    print(id_)
    

if __name__ == "__main__":
    main()
