import numpy as np

# part 1
bintodec = lambda s: int("".join(s.astype(str)),2)
lines = [l.strip() for l in open("./input/input.txt") if l.strip()] 
data = np.array([list(l) for l in lines], int)
gamma = (data.sum(0) > data.shape[0]//2).astype(int)
eps = np.logical_not(gamma).astype(int)
gammad = bintodec(gamma)
epsd = bintodec(eps)
print(gammad*epsd)

def find_points(sign: bool = True):
	Ny, Nx = data.shape
	still_valid = list(range(Ny))
	
	while True:
		for i in range(Nx):
			most_common = int(data[still_valid].T[i].sum() >= len(still_valid)/2)
			for j in still_valid*1:
				if (data[j,i] != most_common) == sign:
					still_valid.remove(j)
				if len(still_valid) == 1:
					break
			if len(still_valid) == 1:
				break
		if len(still_valid) == 1:
			break
	ox = data[still_valid].flatten()
	return ox

ox = bintodec(find_points(True))
co = bintodec(find_points(False))
print(ox*co)
