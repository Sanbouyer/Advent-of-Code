from functools import lru_cache
# Import input.txt as str
with open('input.txt') as input:
    input_text = input.read()


'''
Numerical keypad:
+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+

Directional keypad:
    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+
'''

num_keypad = (('7', '8', '9'),
              ('4', '5', '6'),
              ('1', '2', '3'),
              (None, '0', 'A'))

dir_keypad = ((None, '^', 'A'),
              ('<', 'v', '>'))


@lru_cache  # These functions use the same input many times, so use cache!
def press_number(start_dir: str, dir: str, layers: int) -> int:
    if layers == 0:
        return 1

    # If we have numbers, we need to use the numeric keypad, not the directional keypad
    use_numpad = start_dir.isnumeric() or dir.isnumeric()
    next_dirs = min_path(start_dir, dir, use_numpad) + 'A'
    number = 0
    for i, next_dir in enumerate('A' + next_dirs[:-1]):
        number += press_number(next_dir, next_dirs[i], layers - 1)
    return number


@lru_cache
def min_path(start: str, end: str, numpad: bool) -> list[str]:
    keypad = (dir_keypad, num_keypad)[numpad]
    for i, row in enumerate(keypad):
        if start in row:
            start_indices = (i, row.index(start))
        if end in row:
            end_indices = (i, row.index(end))

    dif = [a[0] - a[1] for a in zip(end_indices, start_indices)]

    # default best directions, we want the same arrows to be next to each other, and the furthest away to be first
    directions = '<' * abs(min(dif[1], 0)) + 'v' * max(dif[0], 0) + \
        '^' * abs(min(dif[0], 0)) + '>' * max(dif[1], 0)

    # Checks to see if the directions go through the empty space, if so, reverse direction
    for i in range(len(directions)):
        dif = (directions[:i + 1].count('v') - directions[:i + 1].count('^'),
               directions[:i + 1].count('>') - directions[:i + 1].count('<'))
        if keypad[start_indices[0] + dif[0]][start_indices[1] + dif[1]] == None:
            return directions[::-1]

    return directions


numerical_codes = input_text.split('\n')

# number of layers, in parts 1 and 2
num_layers = [3, 26]
complexity = [0, 0]

# Same code just different number of layers for both parts so in a loop
for part in range(2):
    for num_code in numerical_codes:
        num_presses = 0
        for i, press in enumerate('A' + num_code[:-1]):
            num_presses += press_number(press, num_code[i], num_layers[part])
        complexity[part] += int(num_code[:-1]) * num_presses


print(complexity[0])
print(complexity[1])
