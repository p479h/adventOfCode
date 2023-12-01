import numpy as np

f =  open("./input/input.txt")
numbers = np.array(f.readline().strip().split(","),int)
tables = np.array([[l.strip().split() for l in L.strip().split("\n")] for L in f.read().strip().split("\n\n")], int)
t = tables.copy()
s = t.shape
def get_winner(table: iter) -> iter:
	for t in table:
		if any(np.any(t.sum(i)==-s[i]) for i in range(0, 2)):
			return t
for i, n in enumerate(numbers):
	t[t==n] = -1
	if not get_winner(t) is None:
		break

winner = get_winner(t)
winner[winner== -1] = 0 
print(winner.sum()*n)
		
		
# Part 2
t = tables.copy()
won = []
for i, n in enumerate(numbers):
	still_playing = [k for k in range(s[0]) if not k in won]
	for j in still_playing:
		t[j,t[j] == n] = -1 
		if any(np.any(t[j].sum(i)==-s[i+1]) for i in range(0, 2)):
			won.append(j)
	if len(won) == s[0]:
		break
i = won.pop(-1)
loser = t[i]
loser[loser == -1] = 0
print(loser.sum()*n)
