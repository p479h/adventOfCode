import re 
import itertools as it 

# Getting file
rules_str, strs = open('data.txt').read().split('\n\n')

## Parsing rules
rules = {}
for id, rule_str in re.findall(r'(\d+): ([ \d\w\|\"]+)$', rules_str, re.MULTILINE):
    if '"' in rule_str:
        rules[id] = rule_str.strip('"')
    elif '|' in rule_str:
        rules[id] = [tuple(re.findall(r'\d+',l)) for l in rule_str.split('|')]
    else:
        rules[id] = tuple(re.findall(r'\d+',rule_str))

def match_message(rules: dict, rule: str|tuple|list, string: str, i: int = 0):
    starting_i = i
    if isinstance(rule, str):
        return rule == string[i], i+1
    if isinstance(rule, tuple):
        for rid in rule:
            is_match, i = match_message(rules, rules[rid], string, i)
            if not is_match:
                return False, starting_i
        return True, i
    elif isinstance(rule, list):
        for rule_tuple in rule:
            is_match, i = match_message(rules, rule_tuple, string, i)
            if is_match:
                return True, i 
        return False, starting_i
    else:
        raise Exception()
    
s = 0
for l in strs.splitlines():
    b, n = match_message(rules, rules['0'], l)
    # print(b and len(l)==n, l)
    s += b and len(l)==n

print(s) # 124