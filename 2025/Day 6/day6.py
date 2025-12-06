# Import input.txt as str
with open('input.txt') as input:
    input_text = input.read()

# input_text = """123 328  51 64
#  45 64  387 23
#   6 98  215 314
# *   +   *   +  """

rows = input_text.split("\n")

problems = rows[0].split()

for row in rows[1:]:
    for j, col in enumerate(row.split()):     # Removes all blank characters
        problems[j] += " " + col


sum_answers = 0
for problem in problems:
    answer = int(problem[-1] == "*")        # 1 if *, 0 if not (+)
    if problem[-1] == "*":
        for op in problem[:-1].split():
            answer *= int(op)
    elif problem[-1] == "+":
        for op in problem[:-1].split():
            answer += int(op)
    sum_answers += answer

print(sum_answers)

# Part 2
sum_answers2 = 0
operands = [""] * len(rows[0])
for row in rows[:-1]:
    for i, col in enumerate(row):
        operands[i] += col.replace(" ", "")

operations = []
for col in rows[-1]:
    if col != " ":
        operations.append(col)

for operation in operations:
    answer = int(operation == "*")
    while operands:
        operand = operands.pop(0)
        if operand == "":
            break

        if operation == "*":
            answer *= int(operand)
        elif operation == "+":
            answer += int(operand)
    sum_answers2 += answer

print(sum_answers2)
