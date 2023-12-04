import matplotlib.pyplot as plt

nums = tuple(map(int,"1,0,15,2,10,13".split(",")))
# Generating first few turns 
turns = [ # Turn, number, past_turn (-1 for first time )
    (i, n, -1) for i,n in enumerate(nums)
]
last_spoken = {n: i for i,n in enumerate(nums)}
spoken = set(nums[:-1])
N =  30000000 
for i in range(len(nums),N+1):
    # Last spoken number 
    n = turns[i-1][1]
    # Finding out if number was spoken before last time(last said set to -1)
    if (last_turn := turns[last_spoken[n]])[2] != -1: 
        # Getting difference in turns
        turn_before = turns[last_turn[2]]
        n = last_turn[0] - turn_before[0]

    else: # First time spoken
        n = 0  

    spoken.add(n) # Updating spoken numbers 
    turns.append((i, n, last_spoken.get(n,-1)))
    last_spoken[n] = i
    
print(turns[N-1])
