from collections import deque 
import numpy as np
import re 

def divisible_by_wrapper(n1: int) -> callable:
	def divisible_by(n2: int) -> bool:
		return (n2%n1) == 0
	#print("Made function divisible by: %i" % n1)
	return divisible_by
	

MAX_ITEMS = 40
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
p = int(np.prod(primes))

class Monke:
	brotherhood = {}
	def __init__(self, 
					name: str,
					items: tuple, 
					operation: callable, 
					test_value: int,
					true_receiver: int,
					false_receiver: int) -> None:
		self.name = name
		self.items = deque(items, MAX_ITEMS)
		self.operation = operation
		self.test_value = test_value
		self.true_receiver = true_receiver
		self.false_receiver = false_receiver
		self.inspection_count = 0
		self.brotherhood[name] = self # Making itself accessible to other monkes 
	
	def play(self) -> "Monke":
		while self.items:
			itemworry = self.items.popleft()
			worryvalue = self.operation(itemworry) 
			worryvalue = worryvalue % p 
			test = worryvalue % self.test_value == 0
			if test:
				m = self.true_receiver
			else:
				m = self.false_receiver
			self.brotherhood[m].items.append(worryvalue)
			self.inspection_count += 1
			#print("Item: %i" % itemworry)
			#print("test: %i using test value %i" % (int(test), self.test_value))
			#print("Threw to: %s" % m)
			
	def __repr__(self) -> str:
		fields = "items operation test_value true_receiver false_receiver inspection_count".split()
		values = [getattr(self, at) for at in fields]
		nfields = len(values)
		subs = tuple(str(v) for field, value in zip(fields, values) for v in (field+":", value))
		return (("Monke %s: \n" % self.name) + "\t%-20s%s\n"*nfields) % subs
	
		
	@classmethod
	def from_text(cls, text: str) -> "Monke":
		getNumbers = lambda l: tuple(
			int(j) for j in l.strip().replace(" ", "").split(",")
			)
		lines = text.split("\n")

		# getting the monkey's name 
		name = int(lines[0].strip("\n:").replace("Monkey ", ""))
		# Getting the items 
		starting_items = getNumbers(
			lines[1].strip("\n:").replace("Starting items: ", "")
			)
		# Getting the operation
		operation_info = lines[2].replace("Operation: new = ", "").strip()
		if "+" in operation_info:
			sign = " + "
		elif "*" in operation_info:
			sign = " * "
		
		def func_gen(operation_info: str):
			def operation_func(old: int) -> int:
				return 	eval(operation_info.replace("old", str(old)))
			#print("Returned function eval(%s)" % operation_info)
			return operation_func
		operation_func = func_gen(operation_info)
		# Getting the test 
		test_value = int(lines[3].replace("Test: divisible by ", "").strip())
		test_func = divisible_by_wrapper(test_value)
		# Getting true func
		true_receiver = int(lines[4].replace("If true: throw to monkey ", "").strip())
		# Getting false func 
		false_receiver = int(lines[5].replace("If false: throw to monkey ", "").strip())
		
		return cls(name, starting_items, operation_func, test_value, true_receiver, false_receiver)
	
