
points = {
    "A": 1, # Rock
    "X": 1,
    "B": 2, # Paper 
    "Y": 2,
    "C": 3, # Scissors
    "Z": 3
    }

ipoints = 0
with open("input.txt", "r") as f:
    for l in f.readlines():
        o, i = l.strip().split()
        o, i = [points[k] for k in [o, i]]
        if i == o: # Draw 
            ipoints += 3

        elif o%3 + 1 == i:# i wins
            ipoints += 6

        ipoints += i
print("The total number of points part 1 is %i" % ipoints)

# Part 2
# If o has to win, i%3 + 1 == o
# If i has to win, o%3 + 1 == i
# Else we tie
ipoints = 0
with open("input.txt", "r") as f:
    for l in f.readlines():
        o, i = l.strip().split()
        o, i = [points[k] for k in [o, i]]
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
    
            
