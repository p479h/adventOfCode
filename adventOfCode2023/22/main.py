import re 
import itertools as it

# Info:
# Maximum per column are 9,9,349 (no need to group them!)
# Z coordinates in same block are sorted!

def main():
    # loading the data     
    bricks = [map(int,re.findall(r"\d+", l)) for l in open("data.txt").read().splitlines()]
    # Formating the data 
    bricks = sorted([list(map(list,zip(b[:3],b[3:]))) for b in map(list,bricks)],
                    key = lambda c: c[2])
    # 
    layer = lambda b: dict((k,list(g)) for k,g in it.groupby(b,key=lambda b: b[-1][0]))
    layers = layer(bricks)

    
    
    return 0

if __name__ == "__main__":
    main()
