# Import input.txt as str
input_text = open('input.txt').read()


def blink(num_list, blinks_done, single_digits, ignore_list: bool = False):
    updated_list = []
    for num in num_list:
        if num in single_digits and not ignore_list:
            single_digits[num][blinks_done] += 1
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


def num_stones(starting_digit: str, blinks_done: int) -> int:
    already_calculated = digit_sizes[starting_digit][blinks_done - 1]
    if already_calculated is not None:
        return already_calculated

    sum_num_stones = 0
    for sub_num, sub_list in digit_self_occ[starting_digit].items():
        for i, num_occ in enumerate(sub_list):
            if num_occ == 0:
                continue
            sum_num_stones += num_occ * num_stones(sub_num, blinks_done - i)

    digit_sizes[starting_digit][blinks_done - 1] = sum_num_stones
    return sum_num_stones


# 25 blinks is small enough that we can brute force
stones = input_text.split(' ')
num_blinks = 25
for blinks_done in range(num_blinks):
    stones = blink(stones, blinks_done, [], True)

print(len(stones))

# For 75 blinks, we need a more complicated caching system
stones = input_text.split(' ')
num_blinks = 75

# Dictionary for each single digit with a list of how many time that digit occurs, after n blinks of the starting input
single_digit_occ: dict[list] = {}

# Dictionary for each single digit, with a single_digit_occ dict, with the key as the starting stone
digit_self_occ: dict[dict[list]] = {}

# Dictionary for each single digit, with list of number of all stones, after n blinks of the digit
digit_sizes: dict[list] = {}

# Setup dictionaries to the right size
for digit in range(10):
    single_digit_occ[str(digit)] = [0] * num_blinks
    digit_self_occ[str(digit)] = {str(num): [0] * 6 for num in range(10)}
    digit_sizes[str(digit)] = [None] * num_blinks

    # Setup digit_sizes
    single_stone = str(digit)
    for i in range(10):
        single_stone = blink(single_stone, 0, [0], True)
        digit_sizes[str(digit)][i] = len(single_stone)

for digit in range(10):
    single_stone = str(digit)
    for blinks_done in range(num_blinks):
        single_stone = blink(single_stone, blinks_done,
                             digit_self_occ[str(digit)], ignore_list=(blinks_done == 0))
        if len(single_stone) == 0:
            break

# Calculate the blinks for the input
for blinks_done in range(num_blinks):
    stones = blink(stones, blinks_done, single_digit_occ)
    if len(stones) == 0:
        break

# Number of stones that have never been through a single digit
number_stones = len(stones)

# Add all stones which ended on a single digit multiplied by the number they would have contributed
for digit, num_occ in single_digit_occ.items():
    number_stones += sum(num_occ[blinks] *
                         num_stones(digit, num_blinks - blinks) for blinks in range(num_blinks))

print(number_stones)
