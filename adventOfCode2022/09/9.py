from Knot import Knot, Rope
from functools import reduce 

data = list(l.strip("\n").split() for l in open("input.txt", "r").readlines())
step_count = reduce(
	lambda v1, v2: int(v1) + int(v2), 
	list(d[1] for d in data))

rope = Rope(10, step_count+1)

for direction, count in data:
	count = int(count)
	for _ in range(count):
		rope.move_along(direction)
	
H = rope.head
T = rope.tail

print("T did %i steps" % len(T.history))
print("H did %i steps" % len(H.history))
print("T visited %i unique spots" % len(set(T.history)))
print("H visited %i unique stops" % len(set(H.history)))
print("H did %i more steps than T" % (len(H.history) - len(T.history)))
