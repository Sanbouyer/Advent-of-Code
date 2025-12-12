# Import input.txt as str
with open('input.txt') as input:
    input_text = input.read()

# input_text = """0:
# ###
# ##.
# ##.

# 1:
# ###
# ##.
# .##

# 2:
# .##
# ###
# ##.

# 3:
# ##.
# ###
# ##.

# 4:
# ###
# #..
# ###

# 5:
# ###
# .#.
# ###

# 4x4: 0 0 0 0 2 0
# 12x5: 1 0 1 0 2 2
# 12x5: 1 0 1 0 3 2"""

parts = input_text.split("\n\n")

# Presents
presents: list[str] = []
for present in parts[:-1]:
    index, shape = present.split(":\n")
    presents.append(shape)

total_fit = 0
for tree in parts[-1].split("\n"):
    tree_size, num_presents = tree.split(": ")
    tree_size = tree_size.split("x")
    num_presents = [int(num) for num in num_presents.split(" ")]

    tree_area = int(tree_size[0]) * int(tree_size[1])
    present_area = sum(num_present*present.count("#")
                       for num_present, present in zip(num_presents, presents))
    if present_area <= tree_area:
        total_fit += 1

print(total_fit)
print("No Part 2: Merry Christmas!")
