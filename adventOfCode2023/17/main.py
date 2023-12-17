from heapq import heappop, heappush

# First tried modifying dijkstra, it did not work... 
# Then tried looking up some answers on reddit, felt inspired by one of them by 
# Strategy was to consider every possible way of travelling in each direction... 
# It did not work. So I tried viewing the difference between my implementation 
# and reddits. The difference was the order of elements in the queue????
# The reason was the use of heapq
# The reason is that heapq returns sorted inputs!
# So if the cost comes first, the next iteration will first consider the path of least resistance!

D = [(0,1),(-1,0),(0,-1),(1,0)] # >^<v (directions)
def travel(graph, min_ = 1, max_= 3):
    h, w = map(len, (graph, graph[0]))
    Q = [(0,0,0,-1)] # cost, i, j, direction last travelled 
    seen = set()
    dist = {} # Distances to each position ((i,j),di) via each direction
    while Q:
        c, i, j, di = heappop(Q)
        if (key:=(i,j,di)) in seen:
            continue 
        seen.add(key)
        # Looping over neighbours
        for ddi,(dy,dx) in ((ddi,dxy) for ddi,dxy in enumerate(D) if di%2!=ddi%2 or di==-1): # Perpendicular direction
            added_c = 0
            for m in range(1,max_+1):
                y, x = i+dy*m, j+dx*m # Getting position after traveling m times along dx,dy
                if not (0<=y<h and 0<=x<w): 
                    break # Skipping outside of domain
                added_c += graph[y][x]
                if m < min_:
                    continue 
                cn = c+added_c
                if dist.get((nkey:=(y, x, ddi)), 1e10) > cn:
                    dist[nkey] = cn 
                    heappush(Q, (cn, y, x, ddi))
    return {(i,j): min(dist.get((i,j,d),1e10) for d in range(4)) 
                 for i in range(h) for j in range(w)}

def main():
    map_ = tuple(tuple(map(int,l)) for l in open("data.txt").read().splitlines())
    h, w = len(map_), len(map_[0])
    # Expecting 1099
    print(travel(map_, 1, 3 )[h-1,w-1])
    print(travel(map_, 4, 10)[h-1,w-1])
    return 0

if __name__ == "__main__":
    main()
