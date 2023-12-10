import string

alphabet = list(string.ascii_lowercase) + list(string.ascii_uppercase)

p = {letter: priority+1 for priority, letter in enumerate(alphabet)}

lines = open("input.txt").read().splitlines()

points = 0
for l in lines:
    middle = len(l)//2
    l0 = set(l[:middle])
    l1 = set(l[middle:])
    points += sum(p[L] for L in l0 if L in l1)
print(points)

# Finding the points for the badges
badge_points = 0
for i, l0 in enumerate(map(set,lines[::3])):
    l1, l2 = map(set, (lines[i*3+1],lines[i*3+2]))
    badge_points += sum(map(p.get, l0&l1&l2))
print(badge_points)
        
