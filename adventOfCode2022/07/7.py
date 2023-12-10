from collections import deque
from classes import File, Directory


# Extracting separate commands 
commands = deque(open("input.txt", "r").read().split("\n$"))

# Removing creatiion of root directory and placing back the "$" signs
root_creation = commands.popleft()
commands = ("$%s" % command.strip("\n") for command in commands)

# Creating root
root = Directory("/", None)

# Looping over commands while swapping cwd
cwd = root
for command in commands:
    cwd = cwd.process_command(command)

# Computing all the sizes
root.compute_size()

# Printing all directories
root.tree()

# Finding sum under thresshold
thresshold = 100000
dirs_under_thress = root.find_dirs_under(thresshold)

# Printing the total size under thresshold 
print(sum(d.size for d in dirs_under_thress))

# Finding directory to delete
disksize = 70000000
requirement = 30000000
taken = root.size
available = disksize - taken
needs = requirement - available

candidates = root.find_dirs_over(needs)
print(min(candidates, key = lambda a: a.size))
