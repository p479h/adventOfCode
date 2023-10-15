from collections import Counter
from pathlib import Path

data_path = Path('./data')
test_data_path = data_path/'test_data.txt'
real_data_path = data_path/'data.txt'

def load_data(path):
    with open(path) as f:
        lines = (l.strip() for l in f.readlines() if l.strip())

    return tuple(map(int, lines))


def main():
    path = [test_data_path, real_data_path][1]
    data = load_data(path)
    sort = [0]+sorted(data)+[max(data)+3]
    diff = [i-j for i,j in zip(sort[1:], sort[:-1])]
    print(Counter(diff))    


if __name__ == "__main__":
    main()
