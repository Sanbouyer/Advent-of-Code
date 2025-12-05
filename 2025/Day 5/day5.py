# Import input.txt as str
with open('input.txt') as input:
    input_text = input.read()

# 348541442870640 too low
# 348541442870650 too low

# input_text = """3-5
# 10-14
# 16-20
# 12-18

# 1
# 5
# 8
# 11
# 17
# 32"""

fresh_IDs, available_IDs = input_text.split("\n\n")

fresh_IDs = fresh_IDs.split("\n")

count_fresh_available = 0

for id in available_IDs.split("\n"):
    for fresh_range in fresh_IDs:
        lower, upper = fresh_range.split("-")
        if int(id) >= int(lower) and int(id) <= int(upper):
            count_fresh_available += 1
            break

print(count_fresh_available)

# Part 2
count_fresh_IDs = 0

non_overlap_fresh_IDs: list[str] = []

for i, fresh_range in enumerate(fresh_IDs):
    lower, upper = fresh_range.split("-")

    for j, fresh_range2 in enumerate(non_overlap_fresh_IDs):
        # Go through non overlapping ids and see where current id range goes
        lower2, upper2 = fresh_range2.split("-")

        if int(lower) >= int(lower2) and int(upper) <= int(upper2):
            # Fully contained don't add
            break

        if int(upper) < int(lower2) - 1:
            # Fully smaller, add before
            non_overlap_fresh_IDs.insert(j, fresh_range)
            break

        if int(lower) <= int(upper2) + 1:

            if int(upper) <= int(upper2):
                non_overlap_fresh_IDs[j] = str(min(int(lower), int(lower2))) + \
                    "-" + upper2
                break

            to_remove: int = 0
            # Check to see if it combines with future ranges since upper > upper2
            for fresh_range3 in non_overlap_fresh_IDs[j+1:]:
                lower3, upper3 = fresh_range3.split("-")

                if int(upper) < int(lower3) - 1:
                    # No overlap
                    non_overlap_fresh_IDs[j] = str(min(int(lower), int(lower2))) + \
                        "-" + upper
                    break
                if int(upper) >= int(upper3):
                    # Full overlap
                    to_remove = non_overlap_fresh_IDs.index(fresh_range3)
                    continue

                non_overlap_fresh_IDs[j] = str(
                    min(int(lower), int(lower2))) + "-" + upper3
                non_overlap_fresh_IDs.remove(fresh_range3)
                break
            else:
                non_overlap_fresh_IDs[j] = str(min(int(lower), int(lower2))) + \
                    "-" + upper
            if to_remove:
                del non_overlap_fresh_IDs[j+1: to_remove + 1]

            break

    else:
        non_overlap_fresh_IDs.append(fresh_range)

# Now count non overlapping ranges

for fresh_range in non_overlap_fresh_IDs:

    lower, upper = fresh_range.split("-")

    count_fresh_IDs += int(upper) - int(lower) + 1

print(count_fresh_IDs)
