# Import input.txt as str
with open('input.txt') as input:
    input_text = input.read()


# input_text = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
# 1698522-1698528,446443-446449,38593856-38593862,565653-565659,
# 824824821-824824827,2121212118-2121212124"""
# input_text.replace("\n", "")


IDranges = input_text.split(",")

sumFakeIDs = 0

for IDrange in IDranges:
    lowerID, upperID = IDrange.split("-")
    for ID in range(int(lowerID), int(upperID) + 1):
        lenID = len(str(ID))
        if lenID % 2 == 0 and str(ID)[:lenID//2] == str(ID)[lenID//2:]:
            sumFakeIDs += ID

print(sumFakeIDs)

sumFakeIDs = 0

for IDrange in IDranges:
    lowerID, upperID = IDrange.split("-")
    for ID in range(int(lowerID), int(upperID) + 1):
        lenID = len(str(ID))
        for repeats in range(2, lenID+1):
            if lenID % repeats != 0:
                continue
            factor = sum([10**i for i in range(0, lenID, lenID//repeats)])
            if ID % factor == 0:
                sumFakeIDs += ID
                break


print(sumFakeIDs)
