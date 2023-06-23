data = tuple(tuple(c.strip().split(" ") for c in l.strip().split("|")) for l in open("./input/input.txt"))

unique_l = {1:2, 4:4, 7:3, 8:7}
unique_n = {v:k for k, v in unique_l.items()} # Length to number
print(sum(int(len(d) in unique_n) for l in data for d in l[1]))

# Part 2
# Building translating dict
mapping = ["abcefg","cf","acdeg","acdfg","bcdf",
		   "abdfg", "abdefg", "acf", "abcdefg", "abcdfg"]
mapset = list(map(set,mapping))
answers = []
for i,(n,k) in enumerate(data):
	known = {unique_n[len(nn)]:set(nn) for j,nn in enumerate(n) if len(nn) in unique_n}
	ANS = []
	for l,v in zip(map(len,k),map(set,k)):
		if l in unique_n:
			ans = unique_n[l]
		elif l == 5:
			if known[7].issubset(v):
				ans = 3
			elif len(v&known[4]) == 3:
				ans = 5
			else:
				ans = 2
		else:
			if known[4].issubset(v):
				ans = 9
			elif known[7].issubset(v):
				ans = 0
			else:
				ans = 6
		ANS.append(ans)
	answers.append(sum(a*10**i for i, a in enumerate(ANS[::-1])))
print(sum(answers))
