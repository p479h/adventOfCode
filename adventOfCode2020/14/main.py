import re 
from pathlib import Path
from itertools import product
from collections.abc import Iterator

data_path = Path('./data')
test_data_path = data_path/'test_data.txt'
real_data_path = data_path/'data.txt'

def load_file(path: str | Path) -> iter:
    with open(path, "r") as f: 
        return map(str.strip, f.readlines())
    
def parse_commands(coms: iter) -> iter:
    command_pat = r"(\w*)(?:\[(\d+)\])?\s=\s([X0-9]*)"
    for c in coms:
        c, i, n = re.findall(command_pat, c)[0]
        if c == "mem":
            i, n = int(i), int(n)
        yield c, i, n


def apply_mask(mask: str, n: int) -> int:
    int2bin = lambda x: format(n,'b').zfill(len(mask))
    return int("".join([x if m=="X" else m for x,m in zip(int2bin(n),mask)]),2)    

def run_program1(commands: Iterator[list[str,str]]) -> int:
    mem = {}
    mask = None 
    for c, i, n in commands:
        if c == "mask":
            mask = n 
            continue 
        mem[i] = apply_mask(mask, n)
    return mem
    
def p1(commands):
    mem = run_program1(commands)
    print(sum(mem.values()))

def apply_mask2(mask: str, num: int) -> int:
    mask = list(mask)
    num_bin = list(format(num,'b').zfill(len(mask)))
    X_indices = [i for i,m in enumerate(mask) if m=="X"]
    n_indices = len(X_indices)
    for bits in product("01", repeat=n_indices):
        for i, b in zip(X_indices, bits):
            num_bin[i] = b
        yield int("".join([m if m=="1" else n for n, m in zip(num_bin, mask)]),2)

def apply_mask3(mask: str, num: int) -> int:
    mask = list(mask)
    num_bin = list(format(num,"b").zfill(len(mask)))
    queue = [(mask,num_bin)]
    while queue:
        mask, num = queue.pop(0)
        if "X" in mask:
            index = mask.index("X")
            for j in (0,1):
                mask[index] = "0"
                num[index] = str(j) 
                queue.append((list(mask), list(num)))
        else:
            yield int("".join([m if m=="1" else n for n, m in zip(num, mask)]),2)


def run_program2(commands: Iterator[list[str,str]]) -> int:
    mem = {}
    mask = None 
    for c, i, n in commands:
        if c == "mask":
            mask = n 
            continue 
        for address in apply_mask2(mask, i):
            mem[address] = n
    return mem
    
def p2(commands):
    mem = run_program2(commands)
    print(sum(mem.values()))

def main():
    path = [test_data_path, real_data_path][1]
    commands = parse_commands(load_file(path))
    p2(commands)

if __name__ == "__main__":
    main()