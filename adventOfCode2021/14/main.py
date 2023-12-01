from collections import Counter
start, rules = open("./input/input.txt").read().split("\n\n")
rules = {k:v for k,v in (rule.strip().split(" -> ") for rule in rules.strip().split("\n"))}
data = list(start)

def increase(start):
	L = len(start)
	for i in range(1,L):
		j = L-i
		pair = "".join(start[j-1:j+1])
		start.insert(j, rules[pair])
	
def count_points(start):
	v = Counter(start).values()
	return max(v) - min(v)
	
prev = 0
for i in range(10):
	increase(data)
	prev = count_points(data)
	
# Part 2
# keep track of existing pairs in dictionaries! 
# Adding a letter adds 2 pairs
data = start
pairs = Counter(map(str.__add__, data, data[1:]))
chars = Counter(data)

for _ in range(40):
	for (a,b), count in pairs.copy().items():
		ins = rules[a+b]
		pairs[a+b] -= count
		pairs[a+ins] += count
		pairs[ins+b] += count
		chars[ins] += count
		
print(max(chars.values())-min(chars.values()))


