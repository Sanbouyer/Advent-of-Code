# Import input.txt as str
input_text = open('input.txt').read()


def escape(text: str, follow_path: bool):
    width = text.find('\n') + 1
    height = len(text) // width
    current_index = text.find('^')
    direction = 0   # This will be mod 4
    previous_indicies = []
    while True:
        if direction == 0:      # Facing up
            col = current_index % width
            obstacle = text[col: current_index: width].rfind('#')
            if follow_path:     # Update text with Xs
                for row in range(obstacle + 1, current_index//width + 1):
                    text = text[:col + row * width] + \
                        'X' + text[col + 1 + row * width:]
            current_index = col + (obstacle+1) * width

        if direction == 2:      # Facing down
            col = current_index % width
            obstacle = text[current_index:: width].find('#')
            if follow_path:     # Update text with Xs
                for row in range(current_index//width, min(obstacle % height + current_index//width, height + 1)):
                    text = text[:col + row * width] + \
                        'X' + text[col + 1 + row * width:]
            current_index += (obstacle - 1) * width

        if direction == 1:      # Facing right
            row = current_index // width + 1
            obstacle = text[current_index: row * width].find('#')
            if follow_path:     # Update text with Xs
                text = text[:current_index] + 'X' * \
                    (obstacle % (width - current_index % width)) + \
                    text[(obstacle % (width - current_index %
                          width)) + current_index:]
            current_index += obstacle - 1

        if direction == 3:      # Facing left
            row = current_index // width + 1
            obstacle = text[(row-1) * width: current_index].rfind('#')
            if follow_path:     # Update text with Xs
                text = text[:obstacle + 1 + (row-1) * width] + 'X' * \
                    (current_index % width - obstacle - 1) + \
                    text[current_index:]
            current_index -= current_index % width - obstacle - 1

        direction = (direction + 1) % 4
        if obstacle == -1:
            return True, text.count('X')
        if current_index in previous_indicies[:-2]:
            return False, text.count('X')
        else:
            previous_indicies.append(current_index)


print(escape(input_text, True)[1])


def block_escape(text):
    blocking_sum = 0
    for i, item in enumerate(text):
        if item in ('#', '^'):
            continue
        blocked_text = text[:i] + '#' + text[i+1:]
        if not escape(blocked_text, False)[0]:
            blocking_sum += 1
    return blocking_sum


print(block_escape(input_text))
