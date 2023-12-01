import re 
from scipy.optimize import fsolve

def main():
	main2()
	
def main2():
	# Solve for everything that does not depend on humn
	known_monkes, other_monkes = load_monkes()
	known_monkes.pop("humn")
	other_monkes["root"][1] = "-" # Return the difference between guess and right value
	km0, om0 = find_all(known_monkes, other_monkes)
	
	def error(i):
		km0["humn"] = i
		km, om = find_all(km0, om0)
		return km["root"]
		
	print(i := int(fsolve(error, 3.58764756e+12, xtol = 0.01)[0]))
	for n in range(i-100, i+100):
		print(error(n), n)
	
	

def main1():
	known_monkes, other_monkes = load_monkes()
	known_monkes, other_monkes = find_all(known_monkes, other_monkes)
	print(known_monkes["root"])
	
def load_monkes():
	# Defining job patterns
	monke_pat = r"[a-z]{4}"
	symbol_pat = "[*/\-+]"

	# Loading all the monkey's info
	known_monkes = {} # Already have known values
	other_monkes = {} # Require info

	for line in open("./inputs/input.txt"):
		monkes = re.findall(monke_pat, line)
		if len(monkes) == 3: # Composite operation
			operation = re.findall(symbol_pat, line)
			other_monkes[monkes[0]] = monkes[1:2]+operation+monkes[2:]
		else:
			known_monkes[monkes[0]] = int(re.findall(r"\d+", line)[0])
	return known_monkes, other_monkes

def find_all(known_monkes: dict, other_monkes: dict):
	# Making copies to not modify originals 
	known_monkes = {m: v for m, v in known_monkes.items()}
	other_monkes = {m: [e for e in exp]  for m, exp in other_monkes.items()}
	# Figuring out what monkes have!
	# removing hmn
	while other_monkes:
		found_monkes = []
		for monke, (m1, sign, m2) in other_monkes.items():
			if m1 in known_monkes and m2 in known_monkes:
				expr = "%i %s %i" % (known_monkes[m1], sign, known_monkes[m2])
				known_monkes[monke] = eval(expr)
				found_monkes.append(monke)
		if not len(found_monkes):
			break
			
		while found_monkes:
			other_monkes.pop(found_monkes.pop())
	return known_monkes, other_monkes


if __name__ == "__main__":
	main()
