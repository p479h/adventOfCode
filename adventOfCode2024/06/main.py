from itertools import product

toi = lambda i: (round(i.real), round(i.imag))
def get(m, i: complex) -> str|None:
    i,j = toi(i)
    return m[i][j] if 0<=i<len(m) and 0<=j<len(m[0]) else None

def get_seen(grid: list[list], ij: complex, d: complex) -> set|None:
    seen=set()
    while not ((wall:=get(grid,ij+d)) is None):
        if (pt:=(toi(ij),toi(d))) in seen: # Checking that current position in seen (pt2)
            return None
        seen.add(pt) # Adding next position to visited
        d /= (1,1j)[wall=='#'] # Rotating -90deg
        ij += (0,d)[wall!='#'] # Updating position
    seen.add((toi(ij),toi(d)))
    return seen

def main():
    # List directions
    dirs = dict(zip('v<^>',(1,-1j,-1,1j)))
    # Load data
    grid = [l.strip() for l in open('data.txt')]
    # Get starting index
    s = complex(*next((i,j)
                      for i,r in enumerate(grid)
                      for j,c in enumerate(r)
                      if c in dirs))
    # Getting starting direction
    ds = dirs[get(grid,s)]
    seen = {u for u,_ in get_seen(grid, s, ds)}

    # Part 2
    count,a,b = 0,0,0
    copy = list(map(list,grid))
    for i,j in seen:
        copy[a][b], copy[a:=i][b:=j] = '.', '#'
        count += (get_seen(copy, s, ds) is None)
        
    print("Pt 1: %i"%len(seen))
    print('Pt 2: %i'%count)
        

if __name__ == "__main__":
    main()
