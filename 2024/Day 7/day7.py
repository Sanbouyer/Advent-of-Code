# Import input.txt as str
with open('input.txt') as input:
    input_text = input.read()


def can_operate(text: str):
    end_value = int(text[:text.index(':')])
    numbers = [int(num) for num in text.split(' ')[1:]]
    cum_values = [[numbers[0]]]
    for num in numbers[1:]:
        cum_values.append([])
        for val in cum_values[-2]:
            cum_values[-1].append(val * num)
            cum_values[-1].append(val + num)
            cum_values[-1].append(val * 10**len(str(num)) + num)
    if end_value in cum_values[-1]:
        return end_value
    else:
        return False


print(sum(can_operate(text) for text in input_text.split('\n')))
