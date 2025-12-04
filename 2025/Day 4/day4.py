# Import input.txt as str
with open('input.txt') as input:
    input_text = input.read()

# input_text = """..@@.@@@@.
# @@@.@.@.@@
# @@@@@.@.@@
# @.@@@@..@.
# @@.@@@@.@@
# .@@@@@@@.@
# .@.@.@.@@@
# @.@@@.@@@@
# .@@@@@@@@.
# @.@.@@@.@."""


width = input_text.find("\n")
neighbour_index = (-width-2, -width-1, -width, -1, 1, width, width+1, width+2)

# Add a border for row overflow. Use "\n" for column overflow
warehouse = "#"*width + "\n" + input_text + "\n" + "#"*width + "\n"

sum_movable = 0

for i, char in enumerate(warehouse):
    if char != "@":
        continue

    # Count 8 neighbours
    neighbours = 0
    for disp in neighbour_index:
        if warehouse[i+disp] == "@":
            neighbours += 1

    if neighbours < 4:
        sum_movable += 1

print(sum_movable)

sum_all_movable = 0
# Use a temporary warehouse since we don't want to remove paper while still counting
new_warehouse = warehouse
while True:
    sum_movable = 0
    for i, char in enumerate(warehouse):
        if char != "@":
            continue

        # Count 8 neighbours
        neighbours = 0
        for disp in neighbour_index:
            if warehouse[i+disp] == "@":
                neighbours += 1

        if neighbours < 4:
            sum_movable += 1
            new_warehouse = new_warehouse[:i] + "x" + new_warehouse[i+1:]

    if sum_movable == 0:
        # No new accessible papers
        break

    sum_all_movable += sum_movable
    warehouse = new_warehouse

print(sum_all_movable)
