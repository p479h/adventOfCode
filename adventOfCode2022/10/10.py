import re
from collections import deque 

X, i = 1, 0
stack = deque([0 for _ in range(3)],3)
record = {0: 1}
def cycle(X, i):
	stack.rotate(-1)
	X, stack[0] = X+stack[0], 0
	record[i+1] = X 
	return X, i+1
for c, n in (re.findall(r"(\w{4})\s*(-?\d*)", l)[0] for l in open("input.txt")):
	if c == "addx":
		stack[2]+=int(n)
		X, i = cycle(X, i)
	X, i = cycle(X, i)
# Part 1
s = sum((k+1)*v for k,v in record.items() if (k+1+20)%40==0)
print(s)

# Part 2
screen = [["." for _ in range(40)] for _ in range(max(record)//40)]
for i, X in record.items():
	lit = {max(X-1,0),X,min(40,X+1)}&{i%40}
	if lit:
		screen[min(i,240)//40][lit.pop()] = "#"
print(*["".join(r) for r in screen], sep="\n")