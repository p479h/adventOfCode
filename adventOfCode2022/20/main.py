import numpy as np
from collections import deque 


# STRATEGY
# each number is associated with an index
# Performing a permutation is equivalent to modifying its index and neighbours
# Special when the new index is equal to lowest index or highest!
# Since all numbers will move away from their starting positions, no numbers will overlap in the end!

# Loading displacements
numbers = [int(l) for l in open("./inputs/input.txt")]
indices = deque(list(range(len(numbers))))
copy = list(range(len(indices)))

decryption_key = 811589153

for i in copy:
	current_i = indices.index(i)
	indices.remove(i) # current_i is unique! so no duplicates
	new_i = (current_i + numbers[i]) % len(indices) 
	indices.insert(new_i, i)
	
# Part 1
new_numbers = [numbers[i] for i in indices]
#print(*new_numbers, sep = " ")
i0 = new_numbers.index(0)
print(sum([new_numbers[(i0+s*1000)%len(numbers)] for s in [1, 2, 3]]), sep = " ")

# Part2 
decryption_key = 811589153
numbers = [n*decryption_key for n in numbers]
indices = deque(list(range(len(numbers))))
copy = [i for i in indices]

for i in indices*10:
	current_i = indices.index(i)
	indices.remove(i) # current_i is unique! so no duplicates
	new_i = (current_i + numbers[i]) % len(indices) 
	indices.insert(new_i, i)
	
new_numbers = [numbers[i] for i in indices]
#print(*new_numbers, sep = " ")
i0 = new_numbers.index(0)
print(sum([new_numbers[(i0+s*1000)%len(numbers)] for s in [1, 2, 3]]), sep = " ")
	
