import re
from math import lcm
import operator as op
import itertools as it
from functools import reduce 

def send_pulse(pulse, src, dst, Q, ntwrk):
    pass

def main():
    ntwrk = {}
    groups = {"%":[], "&":[], "":[]}
    for preffix, src, dst in re.findall(r'([&%]?)(\w+) -> ([, \w]+)', open('data.txt').read()):
        ntwrk[src] = [preffix, eval("[%s]"%re.sub(r"(\w+)", r"'\1'",dst)), 0, {}]
        groups[preffix].append(src)
        # (type of receiver, outlets, on-off, incoming) 

    # Setting all the keys in & to false  
    for pf_conj in groups["&"]:
        for (_, dsts, *_), pf_fl in zip(map(ntwrk.get, groups["%"]), groups["%"]):
            if pf_conj in dsts:
                ntwrk[pf_conj][-1][pf_fl] = (0, 0) # Remembers all low

    # Picking elements that are not in ntwrk keys 
    for missing in set(it.chain.from_iterable(v[1] for v in ntwrk.values()))-set(ntwrk):
        ntwrk[missing] = ("", [], None, {}) # This output works differently! Like an output
    p1 = 0
    pulses = [0,0]
    cycles = []
    for i in range(5000):
        if i == 1000 - 1: # Saving answer for part 1
            p1 = reduce(op.mul, pulses)
        cycles.append(sum(pulses))
        Q = [(0,"button","broadcaster")] # Initially only broadcaster gets low pulse (0)
        while Q:
            pulse, src, dst_name = Q.pop(0)
            dst = ntwrk[dst_name]
            dst[-1][src] = (pulse, dst[-1].get(src,(0,0))[1] or (i+1)*pulse) # Marking last pulse received and when
            pulses[pulse] += 1 # Increasing the pulse count
            # print("%s -%s-> %s"%(src, ["low","high"][pulse],dst_name))
            match dst:
                case "%", dsts, on, _:
                    if not pulse:
                        dst[2] = not on  # Now it swaps between on and off 
                        Q.extend([(not on, dst_name, new_dst_name) for new_dst_name in dsts])
                case "&", dsts, _, h:
                    new_pulse = not all(p[0] for p in h.values())
                    Q.extend([(new_pulse, dst_name, new_dst_name) for new_dst_name in dsts])
                case "", dsts, *_ if dst_name == "broadcaster": 
                    Q.extend([(pulse, dst_name, new_dst_name) for new_dst_name in dsts])
                case "", dsts, *_: # Outputs get caught here  
                    pass
                    # dsts.append(pulse)
    print("Part 1:", p1) # 712543680
    highs = tuple(v[1] for v in ntwrk["vr"][-1].values())
    meet = reduce(lcm, highs) # number of presses required (assuming the cycles are already taking place)!
    print("Part 2:", meet) # 238920142622879 (there might be some error)
    return 0

if __name__ == "__main__":
    main()
