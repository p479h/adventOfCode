from itertools import chain

def travel(contraption: list[list[str]], S: tuple[tuple[int],int] = ((0,0), 0)):
    h, w = len(contraption), len(contraption[0])
    visited = tuple(tuple(set() for _ in range(w)) for r in range(h)) # ((i,j),direction index)
    directions = [(0, 1),(-1, 0),(0, -1),(1, 0)] #>^<v
    Q = [S] # Starts at top right 
    while Q:
        # Picking the current location and direction
        (i,j), d = visit_id = Q.pop()
        
        # Checking that still in bounds and not re-visited
        if not (0<=i<h and 0<=j<w) or visit_id in visited[i][j]: 
            continue
        visited[i][j].add(visit_id)

        # Travelling 
        match contraption[i][j]:
            case x if (x=="." or (x=="-" and d%2==0) or (x=="|" and d%2)):
                di, dj = directions[d]
                Q.append(((i+di,j+dj),d))
            case "-" | "|":
                even, odd = d%2==0, d%2==1
                for dp in (-1, 1): 
                    ddp = dp*(-1, 1)[d//2]
                    Q.append(((i+even*ddp,j+odd*ddp), (d+dp)%4))
            case c: # >/^: 0/1,  ^/>: 1/0,  </v:2/3,  v/<: 3/2
                # Do everything assuming /, flip if \\
                even, odd = d%2==0, d%2==1
                di = (-1,+1)[d//2]
                d  = (d+(-1,1)[even])%4
                if c == "\\":
                    di, d = -di, (d+2)%4
                Q.append(((i+even*di, j-odd*di), d))
    return sum(map(bool, chain(*visited)))


def main():
    contraption = open("data.txt").read().splitlines()
    h, w = len(contraption), len(contraption[0])
    # part 1
    print(travel(contraption))
    
    # Part 2
    print(max(max(travel(contraption,((0  ,j  ),3)) for j in range(0, w)),
              max(travel(contraption,((h-1,j  ),1)) for j in range(0, w)),
              max(travel(contraption,((i  ,0  ),0)) for i in range(0, h)),
              max(travel(contraption,((i  ,w-1),2)) for i in range(0, h))))
    return 0

if __name__ == "__main__":
    main()
