from collections import Counter 

lines = tuple(l.strip("\n") for l in open("input.txt", "r").readlines())

for col in zip(*lines):
    col = "".join(col)
    most_common = Counter(col).most_common(len(set(col))-1) # The remaining is least common
    letter = set(col) - set([mc[0] for mc in most_common])
    for l in letter:
        print(l, end = "")
    
