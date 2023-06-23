data = open("input.txt", "r").read()
groups_by_elf = data.split("\n\n")
cals_by_elf = [sum(int(cals) for cals in g.split("\n") if cals != "") for g in groups_by_elf]

n_max = 3
maxs = []
while (n_max):
    n_max -= 1
    maxs.append(max(cals_by_elf))
    cals_by_elf.pop(cals_by_elf.index(maxs[-1]))

print(sum(maxs))
