from functools import lru_cache

# Import input.txt as str
with open('input.txt') as input:
    input_text = input.read()


# Cache the function since we offen have the same pattern, and sub_patterns is always the same
@lru_cache
def num_ways(pattern: str, sub_patterns: tuple[str]) -> int:
    arrangements = 0
    for sub_pattern in sub_patterns:
        if pattern[:len(sub_pattern)] != sub_pattern:   # The sub_pattern does not fit
            continue

        if pattern == sub_pattern:  # The sub_pattern is exactly the pattern, add one arrangement
            arrangements += 1
        else:                       # Otherwise add the number of arrangements of a recursive smaller pattern
            arrangements += num_ways(pattern[len(sub_pattern):], sub_patterns)

    return arrangements


towels = tuple(input_text.split('\n')[0].split(', '))
patterns = input_text.split('\n')[2:]

possible = 0
sum_perms = 0
for pattern in patterns:
    perms = num_ways(pattern, towels)
    possible += bool(perms)    # Can be done if perm != 0
    sum_perms += perms

print(possible)
print(sum_perms)
