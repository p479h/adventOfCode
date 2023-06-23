import time 
import numpy as np

def bin_count(arr:iter = None, i: int = 0, n: int = 3):
	if arr is None:
		arr = [0 for _ in range(n)]
	if i < n:
		for value in [0, 1]:
			arr[i] = value
			yield from bin_count(arr, i+1, len(arr))
	else:
		yield tuple(i for i in arr)
		
def selective_bin_count(arr:iter = None, i: int = 0, n: int = 3):
	if arr is None:
		arr = [0 for _ in range(n)]
	if i < n and arr[i]:
		for value in [0, 1]:
			arr[i] = value
			yield from selective_bin_count(arr, i+1, len(arr))
	elif i < n: # And not arr[i]
		yield from selective_bin_count(arr, i+1, len(arr))
	else:
		yield tuple(i for i in arr)

		
options = [1, 0, 1, 1, 0]
times = [] 
for i in range(2000):
	t = time.time()
	for o in selective_bin_count(options):
		pass
	times.append(time.time() - t)
	
print(np.mean(times))
