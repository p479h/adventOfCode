from pathlib import Path
from functools import reduce 

data_path = Path('./data')
test_data_path = data_path/'test_data.txt'
real_data_path = data_path/'data.txt'

# Dictionary of displacements
d = {"N": complex(0,1), # Displacement vectors
     "E": complex(1,0),
     "S": complex(0,-1),
     "W": complex(-1,0), 
     "F": complex(1, 0), # Move east (since it is the initial direction)
     "wp": complex(10,1) # Initial waypoint
}

def part1(path):
    # Function to rotate F using e^{i\theta}
    def rotation_func(n):
        def action(p, r):
            d["F"] *= complex(0, 1)**(n*r//90) # Rotate F by nx90deg
            return p
        return action
    rotations = {"R": rotation_func(-1),"L": rotation_func(+1)}
        
    # Displacement functions
    disp_func = lambda k: (lambda p,disp: p + d[k]*disp)
    disps = {k: disp_func(k) for k in d}

    actions = {**rotations, **disps}
    parse_action = lambda p,l: actions[l[0]](p,int(l[1:]))
    
    history = []
    with open(path) as f:
        return reduce(parse_action, f.readlines(), complex(0,0))

def part2(path):
    # Function to rotate F using e^{i\theta}
    def rotation_func(n):
        def action(p, r):
            d["wp"] *= complex(0, 1)**(n*r//90) # Rotate F by nx90deg
            return p
        return action
    rotations = {"R": rotation_func(-1), "L": rotation_func(+1)}

    # Handling displacements
    def disp_func(direction):
        def action(p, disp):
            if direction == "F":
                return p + d["wp"]*disp
            d["wp"] += d[direction]*disp
            return p
        return action
    disps = {k: disp_func(k) for k in d}
    
    actions = {**rotations, **disps}
    parse_action = lambda p,l: [0,actions[l[0]](p,int(l[1:]))][1]
    history = []
    with open(path) as f:
        return reduce(parse_action, f.readlines(), complex(0,0))

    
def main():
    path = [test_data_path, real_data_path][1]
    for part in part1, part2:
        p = part(path)
        print(p, abs(p.real)+abs(p.imag))

if __name__ == "__main__":
    main()
