# Import input.txt as str
with open('input.txt') as input:
    input_text = input.read()

# input_text = """.......S.......
# ...............
# .......^.......
# ...............
# ......^.^......
# ...............
# .....^.^.^.....
# ...............
# ....^.^...^....
# ...............
# ...^.^...^.^...
# ...............
# ..^...^.....^..
# ...............
# .^.^.^.^.^...^.
# ..............."""

input_rows = input_text.split("\n")

start = input_text.find("S")

num_splits = 0
tachyon_beams = set([start])
for row in input_rows:
    for beam in tachyon_beams.copy():
        if row[beam] == "^":
            tachyon_beams.remove(beam)
            tachyon_beams.add(beam - 1)
            tachyon_beams.add(beam + 1)
            num_splits += 1

print(num_splits)

width = input_text.find("\n")
worldlines = {i: 0 for i in range(width)}
worldlines[start] = 1
for row in input_rows:
    for beam in worldlines.keys():
        if worldlines[beam] != 0 and row[beam] == "^":
            worldlines[beam - 1] += worldlines[beam]
            worldlines[beam + 1] += worldlines[beam]
            worldlines[beam] = 0

print(sum(worldlines.values()))
