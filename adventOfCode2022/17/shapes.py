# Loading relevant libraries and functions 
from itertools import product, chain
from os.path import join as path_join
from collections import deque, defaultdict

# Loading the shapes 
shapes_path = path_join("inputs", "shapes.txt")
with open(shapes_path, "r") as f:
	shapes_raw = f.read().strip().split("\n\n")
	
	
# Making shapes into 2d points relative to top left 
SHAPES = deque([], len(shapes_raw))
for shape_raw in shapes_raw:
	shape_points = []
	for i, line in enumerate(shape_raw.split("\n")):
		for j, char in enumerate(line):
			if char == ".":
				continue
			shape_points.append((j, i)) # x then y!
	SHAPES.append(shape_points)
	
# Making bboxes 
mins =  [[min(p[i] for p in s) for i in range(2)] for s in SHAPES]
maxs =  [[max(p[i] for p in s) for i in range(2)] for s in SHAPES]
BBOXES = [[lt, br] for lt, br in zip(mins, maxs)]

# Making shape class for generality
class Shape:
	SHAPES = SHAPES
	BBOXES = BBOXES
	SYMBOLS = "# % @ $ O".split()
	def __init__(self, shape_id: int, x: iter) -> None:
		self.id = shape_id
		self.x = x
		self.xprev = x # Previous position in case of reallocation!
		self.symbol = self.SYMBOLS[self.id]
		self._bin = None # Deque where it resides in field
		
	@property
	def verts(self) -> iter:
		shape = self.SHAPES[self.id]
		return [[x+xx for x, xx in zip(self.x, p)] for p in shape]
		
	@property
	def h(self) -> int:
		return self.bbox[1][1] - self.bbox[0][1]
		
	@property
	def bbox(self) -> iter:
		bbox = self.BBOXES[self.id]
		return [[x+xx for x, xx in zip(self.x, p)] for p in bbox]
		
	@property
	def shape(self) -> iter:
		bbox = self.bbox
		return tuple(bbox[1][i]-bbox[0][i]+1 for i in range(len(bbox)))
		
	def move_back(self) -> None:
		for i in range(len(self.x)):
			self.x[i] = self.xprev[i]
		
	def manhattan(self, shape: "Shape") -> int:
		return sum(abs(xx-pp) for xx, pp in zip(self.x, shape.x))

		
	def overlaps_shape(self, shape: "Shape") -> bool:
		# First check for bbox overlap (more efficient)
		bb0 = self.bbox
		bb1 = shape.bbox
		if any(bb0[1][i] < bb1[0][i] or bb0[0][i] > bb1[1][i] for i in range(2)):
			return False
			
		# Point overlap harder to check so check all pairs
		for V0 in self.verts:
			for V1 in shape.verts:
				if all(v0==v1 for v0, v1 in zip(V0, V1)):
					return True
		return False
	
	def instantiate(self) -> None:
		return self.__class__(self.id, [i for i in self.x])
	
	def overlaps_wallx(self, x: int) -> bool:
		return x in set(p[0] for p in self.verts)
		
	def overlaps_wallsx(self, field: "Field") -> bool:
		return any(self.overlaps_wallx(x) for x in (field.O[0]-1, field.O[0]+field.w))
		
	def overlaps_wallsy(self, field: "Field") -> bool:
		return self.x[1]+self.h >= field.O[1]+field.h
		
	def overlaps_shapes(self, field: "Field") -> bool:
		i = field.shapes.index(self)
		field.shapes.remove(self)
		for s in field.shapes:
			if s.overlaps_shape(self):
				field.shapes.insert(i, self)
				return True
		field.shapes.insert(i, self)
		return False
		
	def overlaps_shapes2(self, field: "Field") -> bool:
		_bin0i = self.x[1]//field._dl
		_bin1i = _bin0i+1
		_bin_1i = _bin0i-1
		bins = _bin_1i, _bin0i, _bin1i
		for s in chain(*[field._bins[i] for i in bins]):
			if s is self:
				continue
			if s.overlaps_shape(self):
				return True
		return False
		
	def __add__(self, v: iter) -> iter:
		for i in range(len(v)):
			self.xprev[i] = self.x[i]
			self.x[i] += v[i]
		return self
		
	def __iadd__(self, v: iter) -> iter:
		return self.__add__(v)
		
	def __sub__(self, v: iter) -> iter:
		for i in range(len(v)):
			self.xprev[i] = self.x[i]
			self.x[i] -= v[i]
		return self
		
	def __isub__(self, v: iter) -> iter:
		return self.__sub__(v)
		
	def __repr__(self) -> str:
		shape = self.shape
		alloc = [list("."*shape[0]) for _ in range(shape[1])]
		for i, j in self.verts:
			alloc[j-self.x[1]][i-self.x[0]] = self.symbol
		s = "\n".join("".join(r) for r in alloc)
		return "Shape:\n x: %s\n Appearance:\n%s" % (str(self.x), s)
		
		
NMAX = 20000
class Field:
	def __init__(self, O: iter, w: int, h: int) -> None:
		self.O = O
		self.w = w
		self.h = h
		self.lims = tuple(i+j for i,j in zip(self.O, (w, h)))
		self.shapes = deque([],NMAX)
		self._dl = 4 # Length of bin!
		self._bins = defaultdict(lambda: [])

	def update_bin(self, shape: "Shape") -> None:
		_bini = shape.x[1]//self._dl
		_bin = self._bins[_bini]
		if _bin is shape._bin:
			return
		elif shape._bin:
			shape._bin.remove(shape)
		_bin.append(shape)
		shape._bin = _bin
		
	def add_shape(self, shape: "Shape") -> None:
		self.shapes.append(shape)
		
	def move_shape_to_start(self, shape: "Shape") -> None:
		# Left edge should be two units to the right of wall!
		shape.x[0] = self.O[0]+2
		
		# Bottom of figure should be 3 units above closest surface
		if len(self.shapes) == 1:
			shape.x[1] = self.h - self.O[1] - 3 - 1 - shape.h
		else:
			i = self.shapes.index(shape)
			self.shapes.remove(shape)
			highest = min(self.shapes, key = lambda s: s.x[1])
			self.shapes.insert(i, shape)
			shape.x[1] = highest.x[1] - 3 - 1 - shape.h
		
		
	def __repr__(self) -> str:
		w, h = self.w, self.h
		# Making the field and its walls 
		s = deque([deque(["."]*(w+2),w+2) for _ in range(h+1)],h+1)
		for i, j in product(range(h+1),range(w+2)):
			y = i - self.O[1]
			x = j - self.O[0]
			if y == h and x in (0, w+1):
				s[y][x]="+"
			elif y == h:
				s[y][x] = "-"
			elif x in (0, w+1):
				s[y][x] = "|"
		
		# Adding the shapes
		for shape in self.shapes:
			for xx,yy in shape.verts:
				y = yy-self.O[1]
				x = xx-self.O[0]
				if 0<=x<w and 0<=y<=(h-1):
					s[y][x+1] = shape.symbol		
		
		s = "\n".join("".join(l) for l in s)
		s += "\nOx-1"+" "*(w-3)+"Ox+w"
		return s
			

		
if __name__ == "__main__":
	ss = [Shape(i, [2, 0]) for i in range(5)]
	field = Field([0, 0], 7, 25)
	for s in ss:
		field.add_shape(s)
		field.move_shape_to_start(s)
		s += [0, 3]
	#ss[0] += [3, 4]
	#ss[1] += [-1, 3]
	#ss[2]+=[-2, 7]
	#ss[-1]+=[3, 8]
	print(field)
	for s in ss:
		print(s.overlaps_shapes(field))
	#print(*ss, sep = "\n\n")
