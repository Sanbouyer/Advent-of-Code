# Import input.txt as str
input_text = open('input.txt').read()

width = input_text.find('\n') + 1
height = len(input_text) // width + 1
freq_dict = {}
for i, letter in enumerate(input_text):
    if letter in ('.', '\n'):
        continue
    pos = (i % width, i // width)
    if letter in freq_dict:
        freq_dict[letter].append(pos)
    else:
        freq_dict[letter] = [pos]

antinode = set()    # Set of tuple antinode positions
for freq, poses in freq_dict.items():
    for posA in poses:
        for posB in poses:
            if posA == posB:
                continue

            x = 2 * posB[0] - posA[0]
            if x >= width - 1 or x < 0:
                continue

            y = 2 * posB[1] - posA[1]
            if y >= height or y < 0:
                continue

            antinode.add((x, y))

print(len(antinode))

antinode = set()    # Set of tuple antinode positions
for freq, poses in freq_dict.items():
    for posA in poses:
        for posB in poses:
            if posA == posB:
                continue
            for i in range(1, max(width, height)):
                x = i * posB[0] - (i-1) * posA[0]
                if x >= width - 1 or x < 0:
                    continue

                y = i * posB[1] - (i-1) * posA[1]
                if y >= height or y < 0:
                    continue

                antinode.add((x, y))
print(len(antinode))
