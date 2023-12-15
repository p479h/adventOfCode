import re 
from functools import reduce

def main():
    sequence = open('data.txt').read()
    
    # Part 1
    HASH = lambda s: reduce(lambda c, s: (c+ord(s))*17%256, s, 0)
    print("Sum HASH: %i"%sum(map(HASH, sequence.split(","))))

    # Part 2
    boxes = [{} for _ in range(256)]
    for step in re.findall(r"(\w+)([\-=])(\d*)", sequence):
        i = HASH(step[0])
        match step:
            case h, "=", d:
                boxes[i][h] = int(d)
            case h, "-", _ if h in (box:=boxes[i]):
                del box[h]

    fp  = sum((i+1)*(j+1)*f
              for i, b in enumerate(boxes)
              for j,f in enumerate(b.values()))
    print("Focusing power: %i"%fp)
    return 0

if __name__ == "__main__":
    main()
