import re
import time 
import itertools as it
from operator import gt, lt


def process_workflow(workflow):
    name, elements = re.findall(r"(\w+)\{([^\}]+)\}", workflow)[0]
    conditions = [
        tuple(filter(bool, re.search(r"(?:(\w+)([<>])(\d+):)?(\w+)", c).groups()))
        for c in elements.split(",")
    ]
    return name, conditions

def process_part(part, workflow):
    for procedure in workflow:
        if len(procedure) == 1: # No test 
            return procedure[0]
        k, comp, n, outcome = procedure 
        if {">":gt, "<":lt}[comp](part[k], int(n)):
            return outcome

def process_rating(part, workflows):
    key = "in"
    while not key in "AR":
        key = process_part(part, workflows[key])
    if key == "A":
        return sum(part.values())
    return 0

def part1(parts, workflows):
    s = 0
    for part in parts:
        s += process_rating(part, workflows)
    print(s) # 378853 your answer is too high, 374873

def part2(workflows):
    # print(workflows["tgz"], parts[0])
    # Building the lists of values where ranges start/end
    splits = {c: [1,4001] for c in "xmas"}
    # Adding the numbers in all workflows 
    for c, s, n, _ in (wf for wfs in workflows.values() for wf in wfs if len(wf)==4):
        splits[c].append(int(n)+(s==">")) 
    # Building a test value for each range and the size of each range 
    TV = [[(a,b-a) for a,b in it.pairwise(r)] for r in map(sorted,splits.values())]
    N = 0
    print(list(map(len,TV)))
    st = time.perf_counter()
    for (x,dx), (m,dm), (a,da), (s,ds) in it.product(*TV):
        part = {"x":x,"m":m,"a":a,"s":s}
        N += dx*dm*da*ds*bool(process_rating(part, workflows))
    et = time.perf_counter()
    print(et - st)
    print(N)

def main():
    # Loading the data 
    workflows, parts = map(str.splitlines, open("test.txt").read().split("\n\n"))
    workflows = dict(map(process_workflow, workflows))
    parts = [eval(re.sub(r"(\w)=", r'"\1":', p)) for p in parts]
    # Part 1
    # part1(parts, workflows) 

    # Part 2 (logic taken from 4HbQ on reddit (this person is insane))
    part2(workflows) # 122112157518711 expected
    return 0

if __name__ == "__main__":
    main()
