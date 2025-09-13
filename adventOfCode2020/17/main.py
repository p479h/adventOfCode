import numpy as np
import itertools as it
from scipy.ndimage import convolve

"""
Coords could be removed if active was not tracked. Instead, just track an ndarray with 0 and 1.
This version of the code is stronger for situations where the cubes are big and sparse
"""

for NDIM in (3,4):
    active: set[tuple[int]] = {
        (*([0]*(NDIM-2)), i, j) 
        for i,r in enumerate(open('data.txt')) 
        for j,c in enumerate(r.strip())
        if c=='#'
    }

    for i in range(6):
        # Making a box of (xyzw coordinates that fully encloses the input)
        limits = [(min(c)-1,max(c)+2) for c in zip(*active)]
        coords = np.mgrid[tuple(it.starmap(slice, limits))]

        # Getting the shape for convenience
        shape = coords.shape[1:]

        # Placing (x,y,z,w) in the last axis for easier looping over
        coords = np.moveaxis(coords,0,-1).reshape(-1,NDIM)

        # Translating active into ndarray for convolution
        active_grid = np.array([tuple(c) in active for c in coords.reshape(-1,NDIM)],int)

        # Making a kernel with a hole in the middle (avoid double counting)
        kernel = np.ones((3,)*NDIM)
        kernel[(1,)*NDIM] = 0

        # Finding number of neigbours
        neigbours = convolve(active_grid.reshape(shape), kernel, cval=0, mode='constant').ravel()

        # Chosing alive/dead next round
        survive = (active_grid&(neigbours==2|(neigbours==3)))|(~active_grid & neigbours==3)

        # Updating active
        for k, k_active in zip(map(tuple, coords), survive):
            if k_active:
                active |= {k}
            else:
                active -= {k}

    # Printing remaining active
    print("Ndim %i: %i"%(NDIM, len(active)))