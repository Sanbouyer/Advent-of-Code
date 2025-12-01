# Import input.txt as str
with open('input.txt') as input:
    input_text = input.read()

# input_text = """L68
# L30
# R48
# L5
# R60
# L55
# L1
# L99
# R14
# L82"""

operations = input_text.split('\n')

dial_size = 100

sum_zeros = 0
dial = 50

for op in operations:
    if op[0] == "L":
        dial -= int(op[1:])
    elif op[0] == "R":
        dial += int(op[1:])
    else:
        print(f"error: {op}")

    if dial % dial_size == 0:
        sum_zeros += 1

print(sum_zeros)

# Part 2
sum_zeros2 = 0
dial = 50

for op in operations:
    for i in range(int(op[1:])):
        if op[0] == "L":
            dial -= 1
        elif op[0] == "R":
            dial += 1
        else:
            print(f"error: {op}")

        if dial % dial_size == 0:
            sum_zeros2 += 1

print(sum_zeros2)
