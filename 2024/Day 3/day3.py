# Import input.txt as str
with open('input.txt') as input:
    input_text = input.read()


def multiply(text: str, enableing: bool):
    sum_mults = 0
    si = text.find('mul(')    # si - starting index
    while si != -1:
        if enableing and text.rfind("do()", 0, si) < text.rfind("don't()", 0, si):
            si = text.find('mul(', si + 7)
            continue
        # First want a 1-3 digit number
        for len_numA in range(1, 4):
            if text[si+4+len_numA] != ',':
                continue
            # Then another 1-3 digit number
            for len_numB in range(1, 4):
                if si+4+len_numA+1+len_numB >= len(text) or text[si+4+len_numA+1+len_numB] != ')':
                    continue
                try:
                    numA = int(text[si+4:si+4+len_numA])
                    numB = int(text[si+4+len_numA+1:si+4+len_numA+1+len_numB])
                except:
                    continue
                sum_mults += numA * numB

        si = text.find('mul(', si + 7)
    return sum_mults


print(multiply(input_text, False))
print(multiply(input_text, True))
