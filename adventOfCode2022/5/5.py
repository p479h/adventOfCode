from collections import defaultdict, deque
import re

MAX_SIZE = 100 # Maximum number of crates 
char_per_box = 3 # Characters per container
move_pat = re.compile(r"move (\d+) from (\d+) to (\d+)")

# Defining a function that swaps the boxes
def move_boxes(number: int, from_id: str, to_id: str, boxes_per_crate: dict) -> None:
    for _ in range(number):
        boxes_per_crate[to_id].append(boxes_per_crate[from_id].pop())

def move_boxes_together(number: int, from_id: str, to_id: str, boxes_per_crate: dict) -> None:
    temp = deque([], MAX_SIZE)
    for _ in range(number):
        temp.append(boxes_per_crate[from_id].pop())
    for _ in range(number):
        boxes_per_crate[to_id].append(temp.pop())

# Allocating "memory"
boxes_per_crate = defaultdict(lambda: deque([],MAX_SIZE))
crates_start = []
ids = None # Will be filled in one of the loops
               
with open("input.txt", 'r') as f:
    lines = (l.strip("\n") for l in f.readlines())
    
    # Constructing boxes
    for l in lines:
        # Break if numbers have been reached
        if l.replace(" ", "").isnumeric():
            # Get numbers and assign to boxes per create 
            ids = l.split()
            
            next(lines) # Skip the empty line
            break

        # Extracting the contents for each number
        mid, stride = int(char_per_box/2), char_per_box+1
        boxes = list(l)[mid::stride]
        if not len(crates_start):
            for box in boxes:
                crates_start.append([])

        for i, box in enumerate(boxes):
            if box: # If not empty
                crates_start[i].append(box)

    # Assigning collected boxes to boxes_per_crate
    for ID, crate in zip(ids, crates_start):
        for box in crate:
            if not box.isspace():
                boxes_per_crate[ID].appendleft(box)

    # Moving boxes
    for l in lines:
        number, from_id, to_id = move_pat.findall(l)[0]
        move_boxes_together(int(number), from_id, to_id, boxes_per_crate)

for ID, crate in boxes_per_crate.items():
    print(crate.pop(), end = "")
