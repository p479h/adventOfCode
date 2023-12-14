import re 
from functools import cache
from itertools import starmap

def f(s:list[str], N: tuple[int]):
    Ns = tuple(map(len, re.findall(r"(?<!#)#+(?!#)", "".join(s))))
    if s.count("#")>sum(N):
        return
    if "?" in s:
        i = s.index("?")
        for fill in ".#":
            yield from f((*s[:i],fill,*s[i+1:]), N)
    else:
        if N == Ns:
            yield 1

# (looked at 4HbQ on reddit)(looked at 4HbQ on reddit)(looked at 4HbQ on reddit)
# (BUT IMPROVED THE CODE SLIGHTLY. He/she had a redundant condition!)
# Better to try index based  (looked up the answer but tried coding myself)
def f2(s: str, N: tuple[int]) -> int: # Taken from 
    """
    Logic:
        If length of string is reached and index of group == len(group_lens), 
            we MUST have gone through all the groups and there are none left (1)
        If the length is reached BUT not all groups are found, we failed (0)
            BOTH can be captured with ni ==  len(N)
        
        If s[si] in ".?" we check if ?=. would be valid and MOVES ON in case 
        it should have been #. 

        At this point the function knows for sure if the string is done OR if ? should have been .
        Now all that is left is to handle a possible group forming, which would require that the 
        PREVIOUS character was . and that the character AFTER the group is not #
        
        So, since we know the size of the current group, we can extract the whole thing and check
        that it contains no '.' inside. And that the following character is not #. If all is
        in order we can complete the group by setting ni+1 and moving to next group. Except...

        then we need to check if the previous character was ".". But here is the catch. We only move to
        the next iteration if the previous group ends in ".". So for every iteration after the first, this
        condition will always be the case! Because if it wasn't we could not nave finished a previous group 
        and therefore there can be no # before the current group. If we are the first iteration that does
        not hold, but the first iteration contains no "#" before that because it is the first iteration.
        So it is all in order.
        The goal then is to take those conditions and accumulate r where recursion is possible 
        and then return the final r, which went through every branch.

        The one thing to note about this function is that in order to avoid the check for a character before
        the group, it must also have checked for a character after the group. So EVERY group must 
        have at least ONE extra trailing character. So the input must have a "." inserted in the end.

        If that is not done, several viable iterations that end in "#" will be discarded.
    """
    # Without cache this function is as slow as my old solution for part 2... 
    # So lesson learned and puzzle 90% solved
    @cache 
    def f(si: int, ni: int, r: int = 0) -> int:
        # Check if ran out of string 
        if si == len(s):
            return ni ==  len(N)
        # Check if we can continue 
        if s[si] in ".?": # Assumes ? to be . and moves on in case it is #
            r += f(si+1, ni)
        # Found a group, trying to read the whole group
        try:
            sj = si + N[ni]
            group = s[si:sj] # only worry is that 
            if (not "." in group) and (not "#" in s[sj]): 
                r += f(sj+1,ni+1)
        except IndexError:
            pass # Don't do anything if there is a wrong index, that just means we failed
        return r
    return f(0,0)
        
def main():
    data = [l.split(" ") for l in open("data.txt").read().splitlines()]
    data = [(l[0], tuple(map(int,l[1].split(",")))) for l in data]
    # Part 1
    print(sum(len(r) for r in map(tuple,starmap(f, data))))

    # Part 2
    print(sum(r for r in starmap(f2, (("?".join([d[0] for _ in range(5)])+".", d[1]*5) for d in data))))
    return 0

if __name__ == "__main__":
    main()
