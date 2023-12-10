data = open("./input.txt").read().split("\n\n")
calls_by_elf = [sum(map(int, g.splitlines())) for g in data]

# Part 1
print(max(calls_by_elf)) # 66487

# Part 2
print(sum(sorted(calls_by_elf)[-3:])) #197301

