import numpy as np
import os

t = open("input.txt", "r").readlines()
table = []
for l in t:
	table.append([])
	for n in l.strip():
		table[-1].append(int(n))

table = np.array(table)

h, w = table.shape
perimeter = 2*(w+h)-4
inner = 0

for i in range(1, h-1):
	for j in range(1, w-1):
		treeh = table[i, j]
		top = table[:i, j]
		bottom = table[i+1:, j]
		left = table[i, :j]
		right = table[i, j+1:]
		for side in top, bottom, left, right:
			if all(treeh>side):
				inner += 1
				break
				
# Printing tree visibility breakdown 
print("Perimeter = %i" % perimeter)
print("Inner = %i" % inner)
print("--------------")
print("Total = %i" % (perimeter + inner))



# Getting the sceninc scores
def get_scenic_score(ij: tuple, table: np.ndarray):
	scores = np.zeros(4, int) # Scores per side
	th = table[ij]
	h, w = table.shape
	I, J = ij
	# Tree to top
	for count, i in enumerate(range(I-1, -1, -1)):
		scores[0] += 1
		if table[i,J] >= th: # If tress height lower than previous tree
			break
	#Tree to bottom
	for count, i in enumerate(range(I+1, w)):
		scores[2] +=1
		if table[i, J] >= th:
			break
	#Tree to left 
	for count, j in enumerate(range(J-1, -1, -1)):
		scores[1] += 1
		if table[I, j] >= th:
			break
	#Tree to right	
	for count, j in enumerate(range(J+1, h)):
		scores[3] += 1
		if table[I, j] >= th:
			break
	return scores.prod()
	
scores = table.copy()*0
for i, row in enumerate(table):
	for j, col in enumerate(row):
		scores[i, j] = get_scenic_score((i,j), table)
		
print("\nThe maximum scenic score was: ")
print(scores.max())





