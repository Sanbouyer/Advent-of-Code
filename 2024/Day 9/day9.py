# Import input.txt as str
input_text = open('input.txt').read()

block_list = []
for ind, num in enumerate(input_text):
    if int(ind) % 2 == 0:
        block_list.extend([int(ind)//2] * int(num))
    else:
        block_list.extend([None] * int(num))

block = block_list.copy()   # A shallow copy for part 2
while True:
    try:
        empty = block_list.index(None)
    except ValueError:
        break
    block_list[empty] = block_list.pop()

print(sum(index * value for index, value in enumerate(block_list)))


for file in range((len(input_text)-1)//2, 0, -1):
    file_size = block.count(file)
    file_index = block.index(file)
    for i in range(block.index(None), file_index - file_size+1):
        small_block = block[i:i+file_size]
        if small_block != [None] * file_size:
            continue
        block[i:i+file_size] = [file] * file_size
        block[file_index:file_index + file_size] = small_block
        break

print(sum(index * value for index, value in enumerate(block) if value is not None))
