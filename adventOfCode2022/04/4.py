from itertools import chain

lines = open("input.txt").read().splitlines()

# Second part
count1 = 0
count2 = 0
for l in lines:
    e0, e1 = [tuple(map(int,e.split("-"))) for e in l.split(",")]

    mi = min(*e0, *e1)
    ma = max(*e0, *e1)
    # Part 1
    if (mi in e0 and ma in e0) or (mi in e1 and ma in e1):
        count1+=1

    # Part 2
    dmax = ma - mi
    # Sorting so e0 has lower bound
    if mi in e1:
        e0, e1 = e1, e0
    # If the difference between higher bound of one and lower bound of other is positive (0 inc) they overlap
    if e0[1] >= e1[0]:
        count2 += 1
        
     
print(count1, count2, sep="\n")
        
