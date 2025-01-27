# Import input.txt as str
with open('input.txt') as input:
    input_text = input.read()


text = input_text

width = text.find('\n')

# Finding XMAS
count = 0
count += text.count('XMAS')                     # Counts forwards
count += text.count('SAMX')                     # Counts backwards

for i in range(width+1):
    count += text[i::width+1].count('XMAS')     # Counts down
    count += text[i::width+1].count('SAMX')     # Counts up

    count += text[i::width+2].count('XMAS')     # Counts diag down right
    count += text[i::width+2].count('SAMX')     # Counts diag up left

    count += text[i::width].count('XMAS')       # Counts diag down left
    count += text[i::width].count('SAMX')       # Counts diag up right

print(count)

# Finding X-MAS
count = 0
indexA = text.find('A', width+2)
while indexA != -1:
    if ((text[indexA - (width+2)] == 'M' and text[indexA + (width+2)] == 'S') or (text[indexA - (width+2)] == 'S' and text[indexA + (width+2)] == 'M')) and ((text[indexA - (width)] == 'M' and text[indexA + (width)] == 'S') or (text[indexA - (width)] == 'S' and text[indexA + (width)] == 'M')):
        count += 1
    indexA = text.find('A', indexA+1, -1 - (width+2))
print(count)
