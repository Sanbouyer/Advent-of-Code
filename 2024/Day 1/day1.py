# Import input.txt as str
with open('input.txt') as input:
    input_text = input.read()

# Then separate into list
input_list = input_text.replace('   ', '\n').split('\n')
# Then separate into two lists
listA, listB = input_list[::2], input_list[1::2]
listA.sort()
listB.sort()

print(sum(abs(int(a)-int(b)) for a, b in zip(listA, listB)))


similarity_sum = 0
for a in listA:
    similarity_sum += int(a)*sum(b == a for b in listB)
print(similarity_sum)
