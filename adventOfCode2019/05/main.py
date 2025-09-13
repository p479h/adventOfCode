import numpy as np
from pathlib import Path
from collections import deque

# Rightmost two values are the opcode (01, 02 or 99)
# Parameter modes are two digits (one per decimal place after opcode read from right to left)
# Instruction: 0102 -> 02 opcode, 1 param, 0 param
# If an instruction requires n parameters, there should be n+2 digits in an instruction
# The leftmost digits are filled with 0
# Writing paramters will always be addresses.
OPCODES = (1,2,3,4)
STORE_ACTION_OPCODES = (1,2)
WRITE_OPCODES = (*STORE_ACTION_OPCODES,3)
NPARAMS = dict(zip(OPCODES,(3,3,1,1)))
ACTIONS = dict(zip(OPCODES,(sum,np.prod,None,None)))
read = lambda index, mode, memory: index if mode else memory[index]
def catch(inst: int):
    opcode = inst%100
    return opcode, [(inst%10**(i+3))//10**(i+2) for i in range(NPARAMS[opcode])]

def part1(n, inputs: deque = deque([])):
    i = 0
    outputs = deque([], 10)
    while (program:=n[i]) != 99:
        # Getting the opcode and nodes for each paramter
        
        opcode, modes = catch(program)
        # Moving the index counter to next opcode and capturing the number of parameters
        i, p_count = i+NPARAMS[opcode]+1, NPARAMS[opcode]
        
        # Getting the parameters
        params = [read(p, m, n) for p,m in zip(n[i-p_count:i], modes)]

        # Getting the correct address 
        if opcode in WRITE_OPCODES:
            params, address = params[:-1], n[i-1]
        else:
            *params, address = params

        # Performing the action
        if opcode in STORE_ACTION_OPCODES:
            assert len(params) == 2, 'Store action opcodes should have two parameters'
            n[address] = ACTIONS[opcode](params)
        elif opcode == 3:
            n[address] = inputs.popleft()
        elif opcode == 4:
            outputs.append(address)
        else:
            raise NotImplementedError()
    print("Program ran with the following outputs %s"%outputs)
    return n[0]


def main():
    data_path = Path(__file__).parent/"data.txt"
    test_data_path = Path(__file__).parent/"test_data.txt"
    data = np.loadtxt(data_path, dtype=int, delimiter=",")
    test_data = np.loadtxt(test_data_path, dtype=int, delimiter=",")

    #data = [data[0], 12, 2, *data[3:]]
    #test_data = [test_data[0], 12, 2, *test_data[3:]] # 1,1,1,4,99,5,6,0,99
    
    # Part 1
    answer1 = part1(data, inputs=deque([1]))
    print("Answer to part 1 is %s"%answer1)

    # Part 1
    #answer2 = part2(data)
    #print("Answer to part 2 is %i,%i, such that 100*noun + verb = %i"%answer2)


if __name__ == "__main__":
    main()
