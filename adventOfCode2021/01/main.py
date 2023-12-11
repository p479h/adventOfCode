# PArt 1
nums = list(map(int, open("./input/input.txt").read().splitlines()))
print(sum(nums[i]-nums[i-1]>0 for i in range(1, len(nums))))

# Part 2
slided = [sum(nums[i-3:i]) for i in range(3,len(nums)+1)]
print(sum(slided[i]-slided[i-1]>0 for i in range(1, len(slided))))


