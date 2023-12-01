from itertools import chain
from classes import Register, Clock, CPU

			
commands = [l.strip("\n") for l in open("input.txt", "r").readlines()]
cpu = CPU()
cpu.add_to_cache(*commands) # Adding commands to cache
print(cpu)
i = cpu.execute()

for _ in i:
	pass
print(cpu.register)
print(cpu.buffer)
