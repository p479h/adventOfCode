

add = lambda a, b: (a[0]+b[0], a[1]+b[1])
def neighbours(pi, pj, connections, dirs, data):
    to = connections[data[pi][pj]][1] # From and to the main
    # Looping over neighbours and the directions to get there
    for i, (ni, nj) in ((i,add(dirs[i],(pi,pj))) for i in to): # looping over neighbours
        # Checking if neighbour is outside 
        if not (0<=ni<len(data) and 0<=nj<len(data[0])):
            continue 
        # Checking if neighbour can receive from pi pj
        from_ = connections[data[ni][nj]][0]
        if i in from_:
            yield (ni, nj)

def dijkstra(graph, S, nf):
    h, w = len(graph), len(graph[0])
    Q = {(i,j) for i in range(h) for j in range(w)} # S, initial direction, distance from S
    dist, prev = [{(i,j): v for i in range(h) for j in range(w)} for v in (1e10, None)]
    dist[S] = 0

    while Q:
        # Collecting the pipe index from queue
        pi = min(Q, key=dist.get)
        Q -= {pi}

        for nij in (n for n in nf(pi) if n in Q):
            if (alt := dist[pi]+1) < dist[nij]:
                dist[nij] = alt
                prev[nij] = pi
    return dist, prev

def draw_pt1(graph, dist, S):
    h, w = map(len, (graph, graph[0]))
    def direction(ij):
        if dist[ij] > 1e9:
            return "."
        if ij == S: 
            return "S"
        return graph[ij[0]][ij[1]]
    
    cycle = [[direction((i,j)) for j in range(w)] for i in range(h)]
    with open("path.txt", "w") as f:
        f.write("\n".join(["".join(l) for l in cycle]))
    return cycle


def count_area(graph, S):
    area = 0
    fp = open('area.txt', "w")
    for i, r in enumerate(graph):
        in_ = False 
        bra = None 
        for j, c in enumerate(r):
            if c in "SLF7J": # S was a patch, NOT A FIX
                if not bra is None:
                    if bra == "F" and c == "J" or \
                       bra == "L" and c == "7":
                        in_ = not in_ 
                if bra == "S": # This could fail on other inputs
                    in_ = not in_
                bra = c
            elif c == "|":
                in_ = not in_
            if c == ".":
                area += in_
                fp.write("OI"[in_])
            else: 
                fp.write(c if c != "S" else "S")
        fp.write("\n")
    return area



def main():
    # Collecting the data 
    data = open("./data.txt").read().splitlines()
    S = [(i,j) for i,r in enumerate(data) for j,c in enumerate(r) if c == "S"][0]
    
    #Defining navigation variables 
    dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)] # Directions <- v -> ^ 
    cons = { # Connections (directions) from which pipe can receive
        "F":((0,3),(1,2)), # (come from), (go to)
        "L":((1,0),(2,3)), 
        "J":((2,1),(3,0)), 
        "7":((3,2),(0,1)), 
        "-":((2,0),(2,0)), 
        "|":((1,3),(1,3)), 
        "S":((0,1,2,3),(0,1,2,3)),
        ".": (tuple(),)*2 # No neighbours 
    } 

    # pt1 
    nf = lambda pi: neighbours(*pi, cons, dirs, data)
    dist, prev = dijkstra(data, S, nf)
    
    # Drawing pt 1 and printing results 
    cycle = draw_pt1(data, dist, S)
    print(max(v for v in dist.values() if v < 1e9))

    # Part 2
    print(count_area(cycle, S)) # 383 is the right answer


    return 0

if __name__ == "__main__":
    main()
