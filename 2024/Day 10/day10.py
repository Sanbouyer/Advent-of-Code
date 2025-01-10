# Import input.txt as str
input_text = open('input.txt').read()

terrain = input_text.replace('\n', '')
width = input_text.find('\n')
height = len(terrain)//width
score = [[0]*width for i in range(height)]


def find_all(text: str, sub: str):
    start = 0
    while True:
        start = text.find(sub, start)
        if start == -1:
            return
        yield start
        # use len(sub) for non-lapping, or 1 for overlapping matches
        start += 1


def reachable_poses(pos, num, count_repeats: bool):
    final_poses = (set(), [])[count_repeats]
    if num == 9:
        if count_repeats:
            final_poses.append(pos)
        else:
            final_poses.add(pos)
        return final_poses

    neigbors_str = (-width, -1, width, 1)
    neigbors_arr = ((-1, 0), (0, -1), (1, 0), (0, 1))

    for i, offset in enumerate(neigbors_arr):
        if pos//width + offset[0] < 0 or pos//width + offset[0] >= height or pos % width + offset[1] < 0 or pos % width + offset[1] >= width:
            continue
        if terrain[pos + neigbors_str[i]] == str(num + 1):
            for s in score[pos//width + offset[0]][pos % width + offset[1]]:
                if count_repeats:
                    final_poses.append(s)
                else:
                    final_poses.add(s)

    return final_poses


def calc_score(count_repeats: bool):
    for num in range(9, -1, -1):
        for pos in find_all(terrain, str(num)):
            score[pos//width][pos %
                              width] = reachable_poses(pos, num, count_repeats)
    print(sum(len(score[pos//width][pos % width])
              for pos in find_all(terrain, str(0))))


calc_score(False)
calc_score(True)
