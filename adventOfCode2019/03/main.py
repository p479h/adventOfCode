import numpy as np
from pathlib import Path
import itertools as it


def parse_data(path):
    parse_direction = lambda s: [dx*int(s[1:]) for dx in {"R":(1,0),"L":(-1,0),"U":(0,1),"D":(0,-1)}[s[0]]]
    lines = []
    for line_pts in open(path):
        line = [[[0,0]]]
        for dxdy in map(parse_direction, line_pts.split(",")):
            O = line[-1][0]
            line[-1].append(dxdy)
            line.append([[O[0]+dxdy[0], O[1]+dxdy[1]]])
        lines.append(np.array(line[:-1], dtype=int))
    return lines

def part1(lines):
    intersections = []
    for (i1,(O1, d1)), (i2,(O2,d2)) in it.product(*list(map(enumerate,lines))):
        # Break if lines are not perpendicular
        if np.dot(d1, d2):
            continue
        t1, t2 = np.linalg.solve(np.transpose([d1, -d2]), O2 - O1)
        if 0<=t1<=1 and 0<=t2<=1:
            yield (lines[0],i1, O1, d1, t1), (lines[1], i2, O2, d2, t2)

def calc_distance_until(line, i, t, dx):
    # Calculating distance until the current movement
    d0 = np.abs(line[:i,1]).sum()

    # Calculating the distance in the current movement
    d1 = np.abs(dx).sum()*t
    return d0+d1
        

def main():
    data_path = Path(__file__).parent/"data.txt"
    test_data_path = Path(__file__).parent/"test_data.txt"
    
    lines = parse_data(data_path)
    # Part 1
    intersections = list(part1(lines))
    distances = sorted(map(int,[np.sum(np.abs(O+dx*t)) for (_,_,O,dx,t),_ in intersections]))
    print("Answer to part 1 is %i"%distances[0])

    # Part 2
    intersections_with_distances = [[(i,t,dx,O,round(calc_distance_until(line,i,t,dx))) for line, i, O, dx, t in intersection] for intersection in intersections]
    s = sorted(intersections_with_distances, key = lambda s: s[0][-1]+s[1][-1])
    print(sum([v[-1] for v in s[0]]))


if __name__ == "__main__":
    main()
