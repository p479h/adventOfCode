x = list(map(int, open("./input/input.txt").read().strip().split(",")))
u = set(x)
minmax = min(u), max(u)
ans = min(range(*minmax), key = lambda v: sum(abs(n-v) for n in x))
print(sum(abs(ans-v) for v in x))

# Part 2
sum_n = lambda v: v*(v+1)//2
ans = min(range(*minmax), key = lambda v: sum(sum_n(abs(n-v)) for n in x))
print(sum(sum_n(abs(ans-v)) for v in x))
