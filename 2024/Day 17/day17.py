import re
import sys

# Import input.txt as str
with open('input.txt') as input:
    input_text = input.read()


def combo(operand: int) -> int:
    if operand == 7:
        print('Combo operand 7 is reserved. Program is not valid')
        sys.exit(1)
    if operand > 3:
        return reg[operand - 4]
    return operand


def execute(opcode: int, operand: int) -> bool | int:

    if opcode == 0:
        reg[0] >>= combo(operand)
    elif opcode == 1:
        reg[1] ^= operand
    elif opcode == 2:
        reg[1] = combo(operand) & 0b111
    elif opcode == 3 and reg[0] != 0:
        return operand
    elif opcode == 4:
        reg[1] ^= reg[2]
    elif opcode == 5:
        out = combo(operand) & 0b111
        outputs.append(out)
        # Used in Part 2 if the output doesn't match the program
        if out != prog[len(outputs) - 1]:
            return False
    elif opcode == 6:
        reg[1] = reg[0] >> combo(operand)
    elif opcode == 7:
        reg[2] = reg[0] >> combo(operand)
    return True


# Uses regex to filter just the numbers
numbers = [int(num) for num in re.findall("[0-9]+", input_text)]
reg, prog = numbers[:3], tuple(numbers[3:])
outputs = []

pointer = 0
while pointer < len(prog):
    val = execute(prog[pointer], prog[pointer + 1])
    if type(val) is bool:
        pointer += 2
    else:
        pointer = val

print(','.join(str(output) for output in outputs))


'''
Part 2:
The Program copies the last 3 bits of A into B and does some stuff to B.
It then removes the last 3 bits of A, outputs B, and repeats.

Since the program is 16 digits long, A must be at least 16 x 3 bits ~ 2.8 e14, so we cannot brute force find it.

However, the lines 7,5,4,4, change B with higher bits in A, up to 7 bits further
We can therefore build A 3 bits at a time, by looking at 2 ** 10 starting values
'''

# Confirmed A's which lead to output being the same as program, up to a certain point
lowest_bits = set((0,))

for index, _ in enumerate(prog):
    new_lowest_bits = set()         # Next set of values which lead to a good output
    for lowest_bit in lowest_bits:  # Iterate over every lowest bit
        for initialA in range(2**10):
            outputs = []            # Fresh run of the program
            reg = [(initialA << (index * 3)) + lowest_bit, 0, 0]
            pointer = 0             # Start the program on the first instruction
            while max(pointer, len(outputs)) < len(prog):
                val = execute(prog[pointer], prog[pointer + 1])
                if val is True:     # Normal, go to next opcode
                    pointer += 2
                elif val is False:  # Output no longer matches prog, break out
                    break
                else:               # Jump to val
                    pointer = val
            if tuple(outputs[:index + 1]) == prog[:index + 1]:
                # If we are on our final index, add the full initalA instead of final 3 bits
                new_lowest_bits.add((((initialA & 0b111), initialA)[index == 15] <<
                                    (index * 3)) + lowest_bit)

    lowest_bits = new_lowest_bits.copy()
    # Quite a slow program, so keeps track of where we are for the user
    print(f'{index + 1}/16 done')

print(min(lowest_bits))
