import re 
from functools import reduce 
from multiprocessing import Pool

# Pt 2 (global for multiprocessing)
def process_range(args):
    (a, b), almanac, lookup = args
    min_ = 1e50
    for n in range(a, a+b):
        min_ = min(min_, reduce(lookup, almanac.values(), n))
    return min_

# Running the numbers 
def lookup(n, ranges):
    for n in (ranges[(a, b)][0] + (n-a) for (a,b) in ranges.keys() if a<=n<=b):
        return n
    return n

def main():
    test_path = "./test.txt"
    data_path = "./data.txt"
    map_ = lambda func, *args: tuple(map(func, *args))
    get_nums = lambda s: map_(int, re.findall(r"\d+", s))

    # Building the alamanac dictionary
    seeds_str, *rest = open(data_path).read().split("\n\n")
    seeds = get_nums(seeds_str)
    almanac = {}
    for name, nums in map_(lambda s: map_(str.strip,s.split(":")), rest):
        almanac[name] = {}
        for a,b,c in map(get_nums,nums.split("\n")):
            almanac[name][(b,b+c-1)] = (a,a+c-1)
    
    # Finding location numbers  (pt 1)
    min_ = min(
        reduce(lookup, almanac.values(), n) 
        for n in seeds
    )
    print(min_)
    
    # Part 2 (takes very long to run!!! HOURS)
    with Pool() as pool:
        min_ = min(pool.map(process_range, [(pair, almanac, lookup) for pair in zip(seeds[0::2], seeds[1::2])]))
    print(min_) # 34039469

    return 0

if __name__ == "__main__":
    main()
