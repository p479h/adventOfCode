import re
import math
from collections import defaultdict

transpose = lambda sq: tuple(zip(*sq))
flip = lambda sq: sq[::-1]
rotate = lambda sq: transpose(flip(sq))

# Confirmed (each square has 4 distinct numbers)
# Each number shows at most 2 times (if a fit was found, it is correct)
data = defaultdict(tuple)
for label, sequence in re.findall(r'Tile (\d+):\n([#.\n]+)(?!=\n)',open('data.txt').read(), re.MULTILINE):
    sequence = tuple(map(tuple,sequence.strip().splitlines()))
    for _ in range(4):
        data[int(label)] += (sequence[0],)
        data[-int(label)] += (sequence[0][::-1],) # Square is flipped
        sequence = rotate(sequence)

# part 1
corners = [k for k in set(map(abs,data)) 
           if sum(s in data[k2] for s in data[k] for k2 in set(data)-{k,-k})==2]
print(corners) 
print(math.prod(corners)) #16192267830719

# Part 2 (assembly)
