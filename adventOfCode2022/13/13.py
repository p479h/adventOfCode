from itertools import zip_longest, chain

# Extracting pars 
with open("input.txt", "r") as f:
	pairs = f.read().strip().split("\n\n")

pairs = [[eval(l) for l in p.split("\n")] for p in pairs]

p = pairs[0]
# Comparing a pair 
def compare(p: iter) -> bool:
	# Unpacking values to compare
	e0, e1 = p
	
	#print("Compare %s and %s" % (e0, e1))
	# If the left runs out first, it is in the right order
	if e0 is None or e1 is None:
		return e0 is None and not e1 is None
		
	# Comparing items of same type
	if type(e0) == type(e1):
		if type(e0) == list:
			for pi in zip_longest(e0, e1, fillvalue = None): # Pair inner 
				# If right ran out, it is in the right order	
				result = compare(pi)
				if not result is None: # None returned in a tie!
					return result
		else: # Integers
			if e0 == e1:
				return None
			return e0 < e1
	else:
		if type(e0) == int:
			e0 = [e0]
		elif type(e1) == int:
			e1 = [e1]
		return compare((e0, e1))
	# If all above fails, e0 == e1, which is a tie!
	return None

s = 0	
for i, p in enumerate(pairs):
	if compare(p):
		s+=i+1
	print("%i was %s" % (i+1, str(compare(p))))

# Functions to sort
def swap(lis: iter, i: int, j: int) -> None:
	temp = lis[j] # Saving j
	lis[j] = lis[i] # Inserting i in j
	lis[i] = temp # inserting j in i
	
# Making system more readable
def should_swap(pair: iter) -> bool:
	# if compare() gives "right" order, must not sort
	return not compare(pair)
	
big_list = list(chain(*pairs, ([[2]],[[6]])))
N = len(big_list)
for i in range(N-1):
	for j in range(i+1, N):
		if should_swap((big_list[i], big_list[j])):
			swap(big_list, i, j)
			
print(*enumerate(big_list), sep = "\n")
		
