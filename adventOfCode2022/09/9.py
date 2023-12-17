from operator import add, mul, sub

D = {"U":(-1, 0), "L":(0,-1), "D": (1, 0), "R":(0, 1)}
def rope_game(N):
	rope = [(0,0) for _ in range(N)]
	top = lambda op, a, b: (op(a[0],b[0]), op(a[1],b[1]))
	beenT = {(0,0):1}
	for d, c in map(str.split, open("./input.txt")):
		for _ in range(int(c)):
			rope[0] = top(add, rope[0], D[d])
			for i in range(1, N):
				r = top(sub, rope[i-1], rope[i]) # Vector from T to H
				if sum(top(mul, r, r)) > 2:
					rope[i] = top(add, rope[i], [i/max(abs(i),1) for i in r])
			beenT[rope[-1]] = 1
	return len(beenT)

print(rope_game(2 ))
print(rope_game(10))

