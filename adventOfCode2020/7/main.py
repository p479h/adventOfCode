from pathlib import Path
import re 

data_path = Path('./data')
test_data_path = data_path/'test_data.txt'
real_data_path = data_path/'data.txt'

def parse_data(path):
    with open(path) as f:
        return (l.strip() for l in f.readlines() if l.strip())

def parse_rule(r):
    pat_parent = r"(\w+ \w+) bags? contain (.*)"
    pat_contain = r"(\d) (\w+ \w+) bags?"
    #pat_not_contain = r"no other bags"

    parent, rest = re.findall(pat_parent, r)[0]
    contains = re.findall(pat_contain, rest)
    return parent, contains

def add_rule(dic, rule):
    parent, contains = rule
    dic[parent] = list(map(lambda a: (int(a[0]), a[1]), contains))


def build_rules(path):
    rules = {}
    data = parse_data(path)
    for row in data:
        rule = parse_rule(row)
        add_rule(rules, rule)

    return rules

def count_bags(rules, kind):
    contained = {}
    not_contained = {}
    contains_count = 0
    for bag_kind, contains in rules.items():
        if not contains:
            not_contained[bag_kind] = 1
            continue 
        copy = [c for c in contains]
        heap = copy
        while heap:
            n, ckind = heap.pop(0)
            if ckind == kind:
                contains_count += 1
                contained[bag_kind] = n
                break
            elif ckind in contained:
                contains_count += 1
                break
            elif ckind in not_contained:
                continue
            elif rules[ckind]:
                searched = list(contained) + list(not_contained)
                not_yet_searched = [
                    c for c in rules[ckind] if not c[0] in searched
                ]
                heap.extend(not_yet_searched)
    return contains_count, contained, not_contained


def count_inside(rules, kind):
    checked = {}
    def count(kind):
        if kind in checked:
            return checked[kind]
        if not rules[kind]:
            checked[kind] = 1
            return 1
        total = sum(n*count(k) for n, k in rules[kind])+1
        checked[kind] = total
        return total
    return count(kind)-1
    
                
            
def main():
    rules = build_rules(real_data_path)
    count, *_ = count_bags(rules, "shiny gold")
    print(count)
    count = count_inside(rules, "shiny gold")
    print(count)
    

if __name__ == "__main__":
    main()
        
