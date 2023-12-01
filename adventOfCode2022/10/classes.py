from collections import deque
from itertools import chain
import numpy as np

COMMAND_DURATIONS = {	
	"addx": 2,
	"noop": 1
}

REGISTER_COMMANDS = ("addx", "noop")
CLOCK_COMMANDS = ("noop",)

class Buffer:
	def __init__(self, w: int = 40, h: int = 6) -> None:
		self.w = w
		self.h = h 
		self.grid = self.build_grid(w, h) # Drawing stage 
		self.sprite = [0, 0] # Position of the drawing "brush"
		
	def build_grid(self, w: int, h: int) -> deque:
		grid = np.full((h, w), ".")
		return grid
		
	def update_sprite(self) -> None: 
		# Moves the sprite by 1 unit each time!
		# If at edges, go to next line 
		ph, pw = self.sprite
		if pw == self.w-1:
			if ph == self.h-1: # End of file !
				return 
			self.sprite = [ph+1, 0]
		else:
			# Move to next spot
			self.sprite = [ph, pw + 1]
			
	def process_pixel(self, x: int, window: int = 3) -> None: 
		# X is the register position
		# Window is the size of the sprite!
		ph, pw = self.sprite
		window_width = window >> 1 # integer division
		if abs(pw-x) <= window_width:
			self.render_pixel(ph, pw)
	
	def render_pixel(self, y: int, x: int, symbol: str = "#") -> None:
		self.grid[y, x] = symbol
		
	def tick(self) -> None:
		self.update_sprite()
		
	def __repr__(self) -> str:
		return "\n".join(["".join(l) for l in self.grid])

class Register:
	def __init__(self) -> None:
		self.value = 1
		self.busy = False # Busy doing something
		self.ticks_left = 0 # Sets the register to free when 0
		self.callback = self.noop # Activates at the end of ticks_left
		
	def process_command(self, command: str, args: iter = []) -> None:
		if self.busy:
			return # Can't do anything mate 
			
		self.busy = True
		self.ticks_left = COMMAND_DURATIONS[command]
		if command == "addx":
			args = int(args[0])
		elif command == "noop":
			pass
		else:
			print("INVALID COMMAND: %s in Register" % command)
			exit()
		f = getattr(self, command)
		self.callback = (lambda: lambda: f(args))()

	def tick(self) -> None:
		if not self.busy:
			return
			
		self.ticks_left -= 1
		if not self.ticks_left:
			self.busy = False
			self.callback()
		
	def addx(self, x: int) -> None:
		self.value += x
		
	def noop(self, *args) -> None:
		pass
	
	def __repr__(self) -> str:
		return "Register:\n\tValue: %i" % self.value

class Clock:
	def __init__(self) -> None:
		self.cycle = 1
		
	def tick(self) -> None:
		self.cycle += 1
		
	def process_command(self, command: str, args: iter) -> None:
		pass
		 
		
class CPU:
	def __init__(self, cache_size: int = 1000) -> None:
		self.clock = Clock()
		self.register = Register()
		self.buffer = Buffer() # w, h set to default in Buffer.__init__
		self.cache = deque([],cache_size) # Cached commands
		
	def calc_signal_strength(self, cycle) -> int:
		return cycle*self.register.value
		
	def parse_command(self, command: str) -> iter:
		split = command.split()
		command = split[0]
		args = None
		if len(split) > 1:
			args = split[1:]
		return command, args 
		
	def execute_command(self, command: str) -> None:
		command, args = self.parse_command(command)
		duration = COMMAND_DURATIONS[command]
		
		# Adding command to register
		self.clock.process_command(command, args)
		self.register.process_command(command, args)
		
		# Awaiting execution of commands 
		for tick in range(duration):	
			self.buffer.process_pixel(self.register.value)
			self.tick()
			yield self
			
	def tick(self) -> None:
		# Makes time pass. 
		# Buffer changes state and clock changes time
		self.buffer.tick() 
		self.register.tick()
		self.clock.tick()
		
	def execute(self, stop: int = 6*40) -> iter: # State of cpu at each cycle
		while self.clock.cycle < stop:
			command = self.cache.popleft()
			yield from self.execute_command(command)
	
	def add_to_cache(self, *commands):
		for command in commands:
			self.cache.append(command)
			
			
	def __repr__(self) -> str:
		fields = "Cycle: RegisterValue: Spritex: Spritey:".split()
		values = self.clock.cycle, self.register.value, self.buffer.sprite[0], self.buffer.sprite[1]
		lw = len(max(fields, key = lambda a: len(a))) + 1
		LW = (lw,)*len(fields)
		subs = tuple(chain(*zip(LW, fields, values)))
		return ("\n".join(["%-*s %i"]*len(fields))) % subs
		
