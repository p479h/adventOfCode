import itertools as it
import operator as op

def main():
    data = [tuple(map(tuple,l.splitlines())) for l in open("./test.txt").read().split("\n\n")]
    # Indexing 
    # 0 0 1 1 2 2 3
    # | . | # | . |
    # s \in (0, nc) e.g. 1, 2
    # c \in [0, nc-1] e.g. 0, 1, 2
    def find_mirror(table, part = 2):
        # Looping over table and its transpose
        for ti, t in enumerate((tuple(zip(*table)), table)):
            nr = len(t) # Number of rows 
            for s in range(1, nr): # Looping over spaces between rows
                n_pairs = min(s, nr-s)
                reflections = tuple(tuple(it.starmap(op.eq,zip(t[s-i-1],t[s+i]))) for i in range(n_pairs))
                similar_cols = tuple(map(all, reflections)) # Identical cols for pair i
                if part == 1: # If we got all good reflections 
                    if all(similar_cols): 
                        return (ti, s) # Cols: 0 Rows: 1, space index
                if part == 2: # If we got all but 1 good reflections and ONLY 1 mismatch
                    if sum(similar_cols) == n_pairs-1 and tuple(it.chain(*reflections)).count(0)==1:
                        return (ti, s) # Cols: 0 Rows: 1, space index

    print(sum(s*((ti+1)%2) + 100*s*ti for ti, s in map(find_mirror, data)))
    return 0

if __name__ == "__main__":
    main()
