from collections import deque 
import numpy as np

class Knot:
	MOVES = {
		"U": (0, 1),
		"D": (0, -1), 
		"R": (1, 0), 
		"L": (-1, 0)
		}
	def __init__(self, nsteps: int) -> None:
		self.p = np.zeros(2, int)
		self.history = deque([tuple(self.p)], nsteps)

		
	def move(self, move: tuple) -> None:
		self.p += move
		self.history.append(tuple(self.p))
		
	def move_along(self, direction: str) -> None:
		move = self.MOVES[direction]
		self.move(move)
	
	def follow(self, knot: "Knot") -> None:
		d = knot.p - self.p
		# If not far enough, no need to move
		if d.dot(d) <= 2:
			return # No need to move
		# Ensure the length of movement along each direction is only 1
		d[np.abs(d)>1]= d[np.abs(d)>1]/np.abs(d[np.abs(d)>1])
		self.move(d)
		
		
class Rope:
	def __init__(self, nknots: int, nsteps: int) -> None:
		self.knots = tuple(Knot(nsteps) for _ in range(nknots))
		self.head = self.knots[0]
		self.tail = self.knots[-1]
	
	def move(self, move: tuple) -> None:
		self.head.move(move)
		self.ripple() # Updating children
			
	def move_along(self, direction: str) -> None:
		self.head.move_along(direction)
		self.ripple() # Updating children
		
	def ripple(self): # Updates child knots
		for i, knot in enumerate(self.knots[1:], start = 1):
			knot.follow(self.knots[i-1])
		
		
