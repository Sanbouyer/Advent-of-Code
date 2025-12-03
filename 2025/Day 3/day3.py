# Import input.txt as str
with open('input.txt') as input:
    input_text = input.read()

# input_text = """987654321111111
# 811111111111119
# 234234234234278
# 818181911112111"""

banks = input_text.split("\n")

sum_joltage = 0

for bank in banks:
    first_digit = max(*bank[:-1])
    first_index = bank.find(first_digit)
    second_digit = max(*bank[first_index+1:])
    sum_joltage += int(first_digit + second_digit)


print(sum_joltage)


num_batteries = 12
sum_big_joltage = 0

for bank in banks:
    nth_index = -1
    for n in range(1, num_batteries):
        nth_digit = max(*bank[nth_index+1:n-num_batteries])
        nth_index = bank[nth_index+1:].find(nth_digit) + nth_index+1
        sum_big_joltage += 10**(num_batteries-n) * int(nth_digit)

    last_digit = max(*bank[nth_index+1:])
    sum_big_joltage += int(last_digit)


print(sum_big_joltage)
