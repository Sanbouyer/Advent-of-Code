# Import input.txt as str
input_text = open('input.txt').read()


def move(warehouse: str, direction: str, width: int, double_width: bool) -> str:
    offset = [-width, 1, width, -1]['^>v<'.find(direction)]
    bot_pos = warehouse.find('@')

    if abs(offset) == 1:    # Moving side to side
        next_space = warehouse[bot_pos + offset::offset].find('.')
        next_wall = warehouse[bot_pos + offset::offset].find('#')
        # No empty space in line, no change in warehouse:
        if next_space == -1 or next_wall < next_space:
            return warehouse

        next_pos = bot_pos + offset * (next_space + 1)
        if offset < 0:  # Pushing left
            return warehouse[:next_pos] + warehouse[next_pos + 1: bot_pos + 1] + '.' + warehouse[bot_pos + 1:]
        # Pushing right
        return warehouse[:bot_pos] + '.' + warehouse[bot_pos: next_pos] + warehouse[next_pos + 1:]

    # Vertical movement

    if warehouse[bot_pos + offset] == '.':  # Empty space, move there
        if offset < 0:
            return warehouse[:bot_pos + offset] + '@' + warehouse[bot_pos + offset + 1: bot_pos] + '.' + warehouse[bot_pos + 1:]
        return warehouse[:bot_pos] + '.' + warehouse[bot_pos + 1: bot_pos + offset] + '@' + warehouse[bot_pos + offset + 1:]

    if not double_width:    # First part, dont have to worry about multiple boxes pushing each other
        next_space = warehouse[bot_pos + offset::offset].find('.')
        next_wall = warehouse[bot_pos + offset::offset].find('#')
        # No empty space in line, no change in warehouse:
        if next_space == -1 or next_wall < next_space:
            return warehouse

        next_pos = bot_pos + offset * (next_space + 1)
        if offset < 0:
            return warehouse[:next_pos] + 'O' + warehouse[next_pos + 1: bot_pos + offset] + '@' + warehouse[bot_pos + offset + 1: bot_pos] + '.' + warehouse[bot_pos + 1:]
        return warehouse[:bot_pos] + '.' + warehouse[bot_pos + 1: bot_pos + offset] + '@' + warehouse[bot_pos + offset + 1: next_pos] + 'O' + warehouse[next_pos + 1:]

    # Going up or down. This is more complicated since a single box can push many more boxes
    pushable = None             # Can the push actually be done? So far we don't know
    # If the push happens what positions will have changed
    changed = [bot_pos]
    # Check row by row. This is the next row of indices to check
    to_check = (bot_pos,)
    while pushable == None:     # Loop until we know if its pushable or not
        new_to_check = set()
        for pos in to_check:
            if warehouse[pos] == '#':
                pushable = False        # A wall blocks the way so the push cannot happen
                # Break out of the for loop and avoid else:
                break
            if warehouse[pos] == '.':
                continue                # We don't need to know about the block above

            new_to_check.add(pos + offset)          # Add block above
            # If it's the left of a box also add right side
            if warehouse[pos + offset] == '[':
                new_to_check.add(pos + offset + 1)
            # And if it's the right of a box, add the left side
            elif warehouse[pos + offset] == ']':
                new_to_check.add(pos + offset - 1)
        else:
            if len(new_to_check) == 0:  # No boxes above, so it must only be '.'
                pushable = True
            to_check = new_to_check     # New layer of positions to check
            # The new layer of blocks will be changed if pushed
            changed.extend(to_check)

    # There is a wall in the way
    if not pushable:
        return warehouse

    # No wall, so we now need to push everything. Do this with lists
    warehouse = list(warehouse)

    for change in reversed(changed):
        # Bottom edge of push doesn't affect or isn't affected by block below.
        if change - offset in changed:
            warehouse[change] = warehouse[change - offset]
            warehouse[change - offset] = '.'

    # Change the list back to str, our function output type
    return ''.join(warehouse)


def count_GPS(warehouse: str, width: int, double_width: bool) -> int:
    start = 0
    count = 0
    while start != -1:
        # Find index of next box
        start = warehouse.find(['O', '['][double_width], start + 1)
        # Add the GPS count to count (x + 100y)
        count += start % width + start // width * 100
    return count + 101 - width  # Remove the start = -1 count that was added


warehouse, directions = input_text.split('\n\n')
width = warehouse.find('\n')
warehouse = warehouse.replace('\n', '')
directions = directions.replace('\n', '')

for direction in directions:
    warehouse = move(warehouse, direction, width, False)

print(count_GPS(warehouse, width, False))


warehouse, directions = input_text.split('\n\n')
# Widen the warehouse: double width and replace strings
width = warehouse.find('\n') * 2
warehouse = warehouse.replace('\n', '').replace('O', '[]').replace(
    '#', '##').replace('.', '..').replace('@', '@.')
directions = directions.replace('\n', '')

for direction in directions:
    warehouse = move(warehouse, direction, width, True)

print(count_GPS(warehouse, width, True))
