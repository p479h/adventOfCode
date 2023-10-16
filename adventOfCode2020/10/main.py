from collections import Counter
from pathlib import Path

data_path = Path('./data')
test_data_path = data_path/'test_data.txt'
real_data_path = data_path/'data.txt'

def load_data(path):
    with open(path) as f:
        lines = (l.strip() for l in f.readlines() if l.strip())

    return tuple(map(int, lines))

def part2(data):
    # Count number of states for each additional element
    states = {data[0]:1}
    for n in data[1:]: # -1 and -2 add states, -3 keeps old number of states
        states[n] =  states.get(n-1,0)+states.get(n-2,0)+states.get(n-3,0) 
    return states[data[-1]]

def main():
    path = [test_data_path, real_data_path][1]
    data = load_data(path)
    sort = [0]+sorted(data)+[max(data)+3]
    diff = [i-j for i,j in zip(sort[1:], sort[:-1])]
    print(Counter(diff))
    print(part2(sort))


if __name__ == "__main__":
    main()
