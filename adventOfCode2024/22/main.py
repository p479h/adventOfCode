import re
import numpy as np
import itertools as it
import collections as C
import matplotlib.pyplot as plt

def drop(bricks):
    # Storing the maximum values of z per x,y coordinate
    peaks = C.defaultdict(int)
    drops = 0

    # Looping over all bricks, trying to lower them, updating peaks and bricks
    for i, (x, y, z, u, v, w) in enumerate(bricks):
        area = [(a,b) for a, b in it.product(range(x, u+1), range(y, v+1))]

        # Highest peak already fallen
        peak = max(peaks[a] for a in area)

        # How much lower the brick can go
        dz = z-peak-1
        drops += bool(dz)

        # Updating the brick position
        bricks[i] = x, y, z-dz, u, v, w-dz

        # Updating the peaks (would be at height w-dz)
        for a in area:
            peaks[a] = w-dz # Setting peak to highest z in block
        
    return drops

def plot_bricks(bricks):
    bricks = np.array(bricks).reshape(-1, 2, 3)
    min_ = bricks.min((0, 1))
    max_ = bricks.max((0, 1))
    xlim, ylim, zlim = zip(min_, max_)
    dx, dy, dz = [lim[1]-lim[0] for lim in zip(min_, max_)]
    brick_array = np.zeros((dx, dy, dz), int)
    for brick in bricks:
        x,y,z,u,v,w = brick.flatten()
        brick_array[x-min_[0]:u-min_[0]+1,
                    y-min_[1]:v-min_[1]+1,
                    z-min_[2]:w-min_[2]+1] = 1

    ax = plt.figure().add_subplot(111, projection="3d")
    ax.voxels(brick_array)
    ax.set_box_aspect([1,1,1])
    

def main():
    # loading the data     
    bricks = [[*map(int,re.findall(r"\d+", l))] for l in open("data.txt")]

    # Sorting based on lowest z
    bricks = sorted(bricks, key=lambda b: b[2]) # We know b[2] <= b[5] from looking at the input

    # Visualizing bricks before
    #plot_bricks(bricks)
    
    # Dropping the bricks
    drop(bricks)

    # Counting number of bricks fallen per brick disintegrated:
    d_per_brick = tuple(map(drop,[[*bricks[:i],*bricks[i+1:]] for i,_ in enumerate(bricks)]))

    s1 = sum(map(lambda b: not b, d_per_brick))
    print("Number of bricks that can be safelty disintegrated:",s1)

    # Counting sum of bricks fallen
    s2 = sum(d_per_brick)
    print(s2)

    # Visualizing bricks after
    #plot_bricks(bricks)
    
    #plt.show()
    
    return 0

if __name__ == "__main__":
    main()
