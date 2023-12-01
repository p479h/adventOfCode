from collections import deque
from classes import Monke
import re 


inputs = open("input.txt", "r").read().split("\n\n")
inputs = [i for i in inputs if i] # Remove empty lines
monkes = [Monke.from_text(i) for i in inputs]

for roundr in range(10000):
	for m in monkes:
		m.play()
		
counts = [m.inspection_count for m in monkes]
print(counts)
print(max(counts))
counts.pop(counts.index(max(counts)))
print(max())
