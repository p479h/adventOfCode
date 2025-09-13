from itertools import combinations, product


def search(w, dI, dJ, I=0, J=0, word="XMAS"):
    # Looping over every element of word and returning if letter is different
    for n, letter in enumerate(word):
        i,j = I+n*dI, J+n*dJ
        if not (0<=i<len(w) and 0<=j<len(w[0]) and letter==w[i][j]):
            return 0
    # If the loop executed with a perfect match on word
    return 1

def searchx(w, I=0, J=0, word='MAS'):
    return sum(search(w, -i,-j, I+i,J+j, word) for i,j in product(*((1,-1),)*2))

def main():
    # Part 1
    directions1 = product(*((0,1,-1),)*2) # Has an added direction (0,0), but it is fast enough anyway.
    data = open('./data.txt').read().splitlines()
    h,w = map(len,(data,data[0]))
    n_matches = sum(
        search(data, *d, *ij, 'XMAS') for d in directions1 for ij in product(*map(range,[h,w]))
    )
    print("%i matches found in part 1"%n_matches)

    # Part 2
    n_matches2 = sum(
        searchx(data, *ij, 'MAS')==2 for ij in product(*map(range,[h,w]))
    )
    print("%i matches were found in part 2"%n_matches2)


if __name__ == '__main__':
    main()
