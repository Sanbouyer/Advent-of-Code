# Import input.txt as str
with open('input.txt') as input:
    input_text = input.read()


def next_secret_num(secret_num: int) -> int:
    # Mult by 64, xor with self, mod 2^24
    secret_num = ((secret_num << 6) ^ secret_num) & 0xFFFFFF
    # Div by 32, xor with self, mod 2^24
    secret_num = ((secret_num >> 5) ^ secret_num) & 0xFFFFFF
    # Mult by 2048, xor with self, mod 2^24
    secret_num = ((secret_num << 11) ^ secret_num) & 0xFFFFFF
    return secret_num


secret_number_generations = 2000
sequence_length = 4

# Convert the str numbers to int
first_numbers = tuple(int(x) for x in input_text.split('\n'))
# buying price of every buyer at every point in the day
prices = tuple([first % 10] for first in first_numbers)
# Dictionary of every sequence as keys with a list of buying prices (and associated buyer)
price_sequences = dict()

sum_after_day = 0
for buyer, secret_number in enumerate(first_numbers):
    # Loop over the whole day
    for i in range(secret_number_generations):
        # Generate new secret numbers
        secret_number = next_secret_num(secret_number)
        # Add the buying price to prices list
        prices[buyer].append(secret_number % 10)
    sum_after_day += secret_number  # sum the final secret number for part A

    # Loop over every buying price for the current buyer
    for i, buy_price in enumerate(prices[buyer][sequence_length:]):
        # Get the sequence of price differences
        sequence = tuple(prices[buyer][i + 1 + j] - prices[buyer][i + j]
                         for j in range(sequence_length))

        # If its a new sequence create new dict item, with tuple (buying price, buyer)
        if sequence not in price_sequences:
            price_sequences[sequence] = [(buy_price, buyer)]
        # If sequence already exists, and hasn't yet occured for the current buyer, add tuple to that list
        # monkey buys on the first sequence occurence, so later ones need to be ignored
        elif price_sequences[sequence][-1][1] != buyer:
            price_sequences[sequence].append((buy_price, buyer))

print(sum_after_day)

max_bananas = 0
for sequence in price_sequences.values():
    # Sum over bananas that can be bought with sequence and update max_bananas if it is bigger
    max_bananas = max(max_bananas, sum(sub_seq[0] for sub_seq in sequence))

print(max_bananas)
