def parse_line(line: str):
	return list(tuple(map(int,p.split(","))) for p in line.strip().split("->"))
	
def parse_file(filename: str = "./input/input.txt") -> iter:
	return list(parse_line(l) for l in open(filename) if l.strip())

def write_point(points: dict, point: iter) -> None:
	if point in points:
		points[point] += 1
	else:
		points[point] = 0
		
def filter_straight(lines: iter) -> iter:
	straight = lambda l: any(a==b for a,b in zip(*l))
	return list(l for l in lines if straight(l))

def get_range(l: iter) -> iter:
	l0, l1 = l
	stepx = 1 if l0[0]-l1[0] < 0 else -1
	stepy = 1 if l0[1]-l1[1] < 0 else -1
	if l0[0] == l1[0]: # Sharing x axis
		yield from ((l0[0],l0[1]+i*stepy) for i in range(abs(l0[1]-l1[1])+1))
	elif l0[1] == l1[1]: # Share y axis
		yield from ((l0[0]+i*stepx,l0[1]) for i in range(abs(l0[0]-l1[0])+1))
	else:
		yield from ((l0[0]+i*stepx,l0[1]+i*stepy) for i in range(abs(l0[0]-l1[0])+1))
		
def run(ranges: iter, ignore_diag: bool = True) -> None:
	points = {}
	for l in filter_straight(ranges) if ignore_diag else ranges:
		for p in get_range(l):
			write_point(points, p)
	print(sum(1 for p,v in points.items() if v))
	return points
	
ranges = parse_file()
run(ranges)
