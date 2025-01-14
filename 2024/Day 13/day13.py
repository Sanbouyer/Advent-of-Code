import numpy as np
# Import input.txt as str
input_text = open('input.txt').read()


# List with string of every arcade game
arcades = input_text.replace('=', '+').replace('\n', ',').split(',,')


def text_to_list(arcade_text: str):
    end = 0
    arcade_info = []
    for i in range(6):
        start = arcade_text.find('+', end)
        end = arcade_text.find(',', start)
        arcade_info.append(arcade_text[start + 1: None if end == -1 else end])
    return arcade_info


def new_basis(arcade_info: list, offset):
    trans_mat = np.array(arcade_info[:4], dtype=int).reshape(2, 2)
    old_vector = np.array(arcade_info[4:], dtype=int) + offset
    new_vector = np.matmul(np.linalg.inv(trans_mat.T), old_vector)
    return new_vector


def tokens_needed(arcades, add_offset=np.array((0, 0))):
    tokens = 0
    for arcade in arcades:
        button_presses = new_basis(text_to_list(arcade), offset=add_offset)
        if abs(button_presses[0] - round(button_presses[0])) + abs(button_presses[1] - round(button_presses[1])) < 0.001 \
                and 0 <= button_presses[0] and 0 <= button_presses[1]:
            tokens += round(button_presses[0]) * 3 + round(button_presses[1])
    return tokens


print(tokens_needed(arcades))
print(tokens_needed(arcades, add_offset=np.array((10000000000000, 10000000000000))))
