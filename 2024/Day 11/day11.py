import numpy as np
# Import input.txt as str
input_text = open('input.txt').read()

stones = input_text.split(' ')
num_blinks = 75


def blink(num_list, blinks_done, popular_occ, ignore_list: bool = False):
    updated_list = []
    for num in num_list:
        if num in popular_occ and not ignore_list:
            popular_occ[num][blinks_done] += 1
            continue
        if ignore_list and num == '0':
            updated_list.append('1')
            continue
        digits = len(num)
        if digits % 2:
            updated_list.append(str(int(num) * 2024))
        else:
            updated_list.append(num[:digits >> 1])
            updated_list.append(str(int(num[digits >> 1:])))
            # str(int()) is to remove leading zeros
    return updated_list


def num_stones(starting_num, blinks_done):
    already_calculated = starting_sizes[str(starting_num)][blinks_done - 1]
    if already_calculated is not None:
        return already_calculated

    sum_num_stones = 0
    for sub_num, sub_list in num_pop_occ[str(starting_num)].items():
        for i, num_occ in enumerate(sub_list):
            if num_occ == 0:
                continue
            sum_num_stones += num_occ * \
                num_stones(sub_num, blinks_done - i)

    starting_sizes[str(starting_num)][blinks_done - 1] = sum_num_stones
    return (sum_num_stones)


popular_occ = {}
num_pop_occ = {}
starting_sizes = {}

# Setup dictionaries
for pop_num in range(10):
    popular_occ[str(pop_num)] = [0] * num_blinks
    num_pop_occ[str(pop_num)] = {str(num): [0] * 6 for num in range(10)}
    starting_sizes[str(pop_num)] = [None] * num_blinks
    single_stone = str(pop_num)
    for i in range(10):
        single_stone = blink(single_stone, 0, [0], True)
        starting_sizes[str(pop_num)][i] = len(single_stone)

for pop_num in range(10):
    single_stone = str(pop_num)
    for blinks_done in range(num_blinks):
        single_stone = blink(single_stone, blinks_done,
                             num_pop_occ[str(pop_num)], ignore_list=(blinks_done == 0))
        if len(single_stone) == 0:
            break

for blinks_done in range(num_blinks):
    stones = blink(stones, blinks_done, popular_occ)
    if len(stones) == 0:
        break

number_stones = len(stones)
for num in range(10):
    number_stones += sum(popular_occ[str(num)][blinks] *
                         num_stones(num, num_blinks - blinks) for blinks in range(num_blinks))

print(number_stones)
