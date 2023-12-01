from collections import deque

# Part 1
data = list(map(int,open("./input/input.txt").read().strip().split(",")))
remaining = deque([0 for i in range(9)])
for time in data:
	remaining[time] += 1

# Evolving in time 
for i in range(256): # 80 days
	n = remaining.popleft()
	remaining.append(n)
	remaining[6] += n
	
print(sum(remaining))
