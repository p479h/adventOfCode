import re 
from pathlib import Path

data_path = Path('./data')
test_data_path = data_path/'test_data.txt'
real_data_path = data_path/'data.txt'

def parse_data(path):
    with open(path) as f:
        lines = (l.strip() for l in f.readlines() if l.strip())
    
    pat = r"(\w{3}) \+?(-?\d+)"
    f = lambda d: [d[0], int(d[1])]
    return [f(re.findall(pat, l)[0]) for l in lines]

def loop(inst):
    acc = 0
    comi = 0
    clock = 0
    visit_tracker = [[] for _ in inst]
    def process_command(command, number):
        nonlocal acc, clock, comi
        clock += 1
        visit_tracker[comi].append((clock, acc))
        if command == "jmp":
            comi += number
            return
        elif command == "acc":
            acc += number

        # Either acc or nop will just move on
        comi += 1

    while comi < len(inst) and max(len(a) for a in visit_tracker) < 2:
        command, number = inst[comi]
        process_command(command,number)
    return comi, visit_tracker

def find_accumulator_at_bug(visits):
    for v in filter(bool, visits):
        if len(v) == 2:
            return v[-1][-1]

def find_bug(inst):
    for i, (com, n) in enumerate(inst):
        if not com in ("nop", "jmp"):
            continue
        orig = com
        inst[i][0] = "nop" if com == "jmp" else "jmp"
        comi,tracker = loop(inst)
        if comi >= len(inst):
            return max(*tracker,
                       key = lambda c: c[0][0] if c else -1) 
        inst[i][0] = orig

def main():
    data = parse_data(real_data_path)
    _, visits = loop(data)
    acc = find_accumulator_at_bug(visits)
    bug = find_bug(data)
    comi, acc = bug
    print(acc)

if __name__ == "__main__":
    main()

    
