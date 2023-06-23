import string


alphabet = list(string.ascii_lowercase) + list(string.ascii_uppercase)

p = {letter: priority+1 for priority, letter in enumerate(alphabet)}

points = 0

with open("input.txt", "r") as f:
    for l in f.readlines():
        l = l.strip() # Removing trailing \n
        middle = int(len(l)/2)
        l0 = set(l[:middle])
        l1 = set(l[middle:])
        points += sum(p[L] for L in l0 if L in l1)

print(points)

# Finding the points for the badges
badge_points = 0
with open("input.txt", "r") as f:
    lines = f.readlines()
    for i, l0 in enumerate(lines[::3]):
        l0 = set(l0.strip())
        l1 = set(lines[i*3+1].strip())
        l2 = set(lines[i*3+2].strip())
        badges = l0&l1&l2
        for b in badges:
            badge_points += p[b]

print(badge_points)
        
