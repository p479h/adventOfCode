
points = {
    "A": 1, # Rock
    "X": 1,
    "B": 2, # Paper 
    "Y": 2,
    "C": 3, # Scissors
    "Z": 3
    }

lines = open("input.txt").read().splitlines()
ipoints = 0
for l in lines:
    o, i = map(points.get, l.split())
    ipoints += (3 if i==o else 6 if o%3+1==i else 0) + i
print("The total number of points part 1 is %i" % ipoints)

# Part 2
# If o has to win, i%3 + 1 == o
# If i has to win, o%3 + 1 == i
# Else we tie
ipoints = 0
for l in lines:
    o, i = map(points.get, l.split())
    # Assigning i
    if i == 1: # I need to lose (o wins)
        i = (o-2)%3 + 1
    elif i == 2: # I need to draw
        i = o
        ipoints += 3
    else: # I need to win
        i = o%3 + 1
        ipoints += 6
    ipoints += i
print(ipoints)
    
            
