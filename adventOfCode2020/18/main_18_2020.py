import re 

rep = lambda s: str(eval(s.group()))

def reduce_simple(s, precedence: tuple[tuple[str]]):
    assert not set('()')&set(s)
    # Match each group of priority operators
    for prios in precedence: # signs in each prios have the same priority
        # While these operators exist in s
        prio_pat = '[\\%s]'%(''.join(prios))
        while re.search(prio_pat, s):
            # Replace them from left to right
            match = re.search(r'\d+ %s \d+'%prio_pat, s)
            s = s.replace(match.group(), rep(match), 1)
    return s

def digest(s, precedence):
    par_pat = r'\([^\(\)]+\)'
    # Processing inner ()
    while ')' in s:
        s = re.sub(par_pat, lambda c: reduce_simple(c.group()[1:-1], precedence), s)
    # Converting result to int
    return int(reduce_simple(s, precedence))

def reduce1(s): 
    return int(digest(s, ([r'\*',r'\+'],)))

def reduce2(s): 
    return int(digest(s, (['+'],['*'])))

print(sum(map(reduce1, open('data.txt')))) # 6811433855019
print(sum(map(reduce2, open('data.txt')))) # 129770152447927 
