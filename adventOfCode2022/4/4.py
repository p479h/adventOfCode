
count = 0
with open("input.txt", "r") as f:
    lines = f.readlines()
    for i, l in enumerate(lines):
        # Get ranges
        e0, e1 = l.strip("\n").split(",")
        e0, e1 = [tuple(int(v) for v in e.split("-")) for e in [e0, e1]]
                
        #Arrange such that at least one elf has both bounds
        mi = min(*e0, *e1)
        ma = max(*e0, *e1)
        if (mi in e0 and ma in e0) or (mi in e1 and ma in e1):
            count+=1
        
print(count)

# Second part
count = 0
with open("input.txt", "r") as f:
    lines = f.readlines()
    for i, l in enumerate(lines):
        e0, e1 = l.strip("\n").split(",")
        e0, e1 = [tuple(int(v) for v in e.split("-")) for e in [e0, e1]]

        mi = min(*e0, *e1)
        ma = max(*e0, *e1)
        dmax = ma - mi

        # Sorting so e0 has lower bound
        if mi in e1:
            e0, e1 = e1, e0

        # If the difference between higher bound of one and lower bound of other is positive (0 inc) they overlap
        if e0[1] >= e1[0]:
            count += 1
        
     
print(count)
        
