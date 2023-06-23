# Part 1
addt = lambda t0, t1: (t0[0]+t1[0],t0[1]+t1[1])
mul = lambda v, t: (t[0]*v, t[1]*v)
directions = {"forward": (1, 0), "down": (0, 1), "up": (0, -1)}
lines = [l.strip().split() for l in open("./input/input.txt") if l.strip()]
commands = [mul(int(l[1]),directions[l[0]]) for l in lines]
x = (0, 0)
for c in commands:
	x = addt(x, c)


# Part 2
x = [0, 0, 0]
for c, n in map(lambda a: (a[0], int(a[1])), lines):
	if c == "forward":
		x[0] += n
		x[1] += n*x[2]
	elif c == "down":
		#x[1] += n
		x[2] += n
	else:
		#x[0] += n
		x[2] -= n
		
print(x[0]*x[1])
