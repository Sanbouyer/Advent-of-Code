# Import input.txt as str
with open('input.txt') as input:
    input_text = input.read()

rules_text, updates_text = input_text.split('\n\n')

rules = {}
rules_list = rules_text.replace('|', '\n').split('\n')

for i, before in enumerate(rules_list[::2]):
    try:
        rules[before].append(rules_list[2*i+1])
    except KeyError:
        rules[before] = [rules_list[2*i+1]]


def check_update(update: str, reorder: bool):
    pages = update.split(',')
    for i, page in enumerate(pages[1:]):
        for j, prev_page in enumerate(pages[:i+1]):
            try:
                if prev_page in rules[page]:
                    if not reorder:
                        return False
                    pages[j] = page
                    pages[i + 1] = prev_page
                    return check_update(','.join(pages), True)
            except KeyError:
                continue
    return int(pages[(len(pages) - 1)//2])


no_reordering = sum([check_update(update, False)
                    for update in updates_text.split('\n')])
print(no_reordering)

reordering = sum([check_update(update, True)
                 for update in updates_text.split('\n')])
print(reordering - no_reordering)
