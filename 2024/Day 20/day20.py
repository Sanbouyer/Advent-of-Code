# Import input.txt as str
with open('input.txt') as input:
    input_text = input.read()

# input_text = '''###############
# #...#...#.....#
# #.#.#.#.#.###.#
# #S#...#.#.#...#
# #######.#.#.###
# #######.#.#...#
# #######.#.###.#
# ###..E#...#...#
# ###.#######.###
# #...###...#...#
# #.#####.#.###.#
# #.#...#.#.#...#
# #.#.#.#.#.#.###
# #...#...#...###
# ###############'''


class Path:
    def __init__(self, neighbours: tuple[int], indices: list):
        self.indices = indices
        self.neighbours = neighbours

    def find_next(self, maze: str) -> bool | list[object]:
        """Does a generation of the path object, finding the next possible directions it can go and updating the number of steps.

        Args:
            obstacles (tuple[int]): tuple of indices of where there are obstacles which would block the path
            min_steps (list): The smallest number of steps to reach the index.
                              Used to remove non optimal paths without recalculating all future paths from there.

        Returns:
            True: if the end (size) has been reached
            False: if it is a dead end or the path is not optimal
            list[object]: List containing new path objects spawned from a crossroads
        """
        if maze[self.indices[-1]] == 'E':  # Reached the end
            return True

        # Finds list of possible directions path can take
        for offset in self.neighbours:
            if maze[self.indices[-1] + offset] == '#':  # Can't go through wall
                continue
            if maze[self.indices[-1]] == '.' and self.indices[-1] + offset == self.indices[-2]:
                continue
            # If on adding the offset would lead to going over the edge, continue
            break

        # Update self
        self.indices.append(self.indices[-1] + offset)
        return False


def cut_offsets(cheat_length: int, width: int):
    offsets = []
    for x in range(-cheat_length, cheat_length + 1):
        for y in range(-cheat_length + abs(x), cheat_length - abs(x) + 1):
            offsets.append((x * width + y, abs(x) + abs(y), y))

    return tuple(offsets)


width = input_text.find('\n')
maze = input_text.replace('\n', '')
neighbours = (-width, 1, width, -1)

# Find the normal path of maze
path = Path(neighbours, [maze.find('S')])
for i in range(10000):
    if path.find_next(maze):    # We have reached then end if it returns True
        break

normal_path = tuple(path.indices)

min_time_save = 100

simple_cheat_length = 2
complex_cheat_length = 20

simple_cuts = 0
complex_cuts = 0

simple_offsets = cut_offsets(simple_cheat_length, width)

for i, start_cut in enumerate(normal_path[:-min_time_save]):

    # For the simple shortcut, it is better to iterate over area we can shortcut to
    for offset in simple_offsets:
        # Check to see if we go over the edge
        if start_cut // width != (start_cut + offset[2]) // width:
            continue
        # if the offset is late enough along normal path, it saves us enough time
        if start_cut + offset[0] in normal_path[i + min_time_save + offset[1]:]:
            simple_cuts += 1

    # For the longer shortcut, it is better to iterate over all later paths which would save us the required time.
    for j, end_cut in enumerate(normal_path[i + min_time_save:]):
        y = (end_cut // width) - (start_cut // width)       # Height of cut
        x = (end_cut % width) - (start_cut % width)         # Width of cut
        if abs(x) + abs(y) <= min(j, complex_cheat_length):
            complex_cuts += 1

print(simple_cuts)
print(complex_cuts)
