from pathlib import Path

data_path = Path('./data')
test_data_path = data_path/'test_data.txt'
real_data_path = data_path/'data.txt'

def part1(path):
    with open(path) as f:
        t0 = int(f.readline())
        bus_list = f.readline().strip().split(",")
        busses = list(map(int,filter(lambda s: s.isnumeric(), bus_list)))

    t = t0
    while not any(not(t%b) for b in busses):
        t += 1
    # Getting the bus
    for b in busses:
        if not (t%b):
            break
    print("Wait is %i minutes and bus %i"%(t-t0,b))


def part2(path):
    # Loading the data 
    with open(path) as f:
        t0 = 0
        f.readline()
        bus_list = f.readline().strip().split(",")
        
    # Adding the ids to the busses 
    buswithids = enumerate(bus_list)
    # Selecting busses that don't have x's
    buswithids = filter(lambda ib: ib[1].isnumeric(), buswithids)
    # Converting getting factors (bus+index)
    periods = list(map(lambda ib: (ib[0],int(ib[1])),buswithids))

    # Picking the step of t that ensures the first bus is on time
    def next_periods(start, step):
        i = -1
        while True:
            i += 1
            yield start + i*step
    dt = 1
    t = periods[0][1] # Skip trivial solution (t=0)
    # Once we find the period of the first bus we can start moving in first bus periods
    # Once we find the second bus we can move in their combined period... So on until the last bus
    for i,b in periods:
        # Finding the period where the bus will arrive
        t = next(t_ for t_ in next_periods(t, dt) if (t_+i)%b == 0)
        dt *= b
    print("Wait is %i minutes with moduli"%t)


def main():
    path = [test_data_path, real_data_path][1]
    part2(path)


if __name__ == "__main__":
    main()
        
