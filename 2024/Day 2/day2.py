# Import input.txt as str
with open('input.txt') as input:
    input_text = input.read()

# Then separate into list
reports = input_text.split('\n')


def is_safe(report):
    if isinstance(report, str):
        report = [int(i) for i in report.split(' ')]
    is_increasing = report[1] - report[0] > 0
    lb, ub = [-3, 1], [-1, 3]
    for i, next in enumerate(report[1:]):
        if next - report[i] > ub[is_increasing] or next - report[i] < lb[is_increasing]:
            return False
    return True


def problem_dampener(report_str: str):
    levels = [int(i) for i in report_str.split(' ')]
    for i in range(len(levels)):
        removed_level = levels.pop(i)
        if is_safe(levels):
            return True
        levels.insert(i, removed_level)
    return False


print(sum(is_safe(report) for report in reports))

print(sum(problem_dampener(report) for report in reports))
