import sys
# Import input.txt as str
with open('input.txt') as input:
    input_text = input.read()


class Path:
    def __init__(self, neighbours: tuple[int], indices: list, steps: int):
        self.indices = indices
        self.neighbours = neighbours
        self.steps = steps

    def find_next(self, obstacles: tuple[int], size: tuple[int], min_steps: list) -> bool | list[object]:
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
        if self.indices[-1] == size[0] * size[1] - 1:  # Reached the end
            return True
        # This path is better, update min_scores
        if min_steps[self.indices[-1]] > self.steps:
            min_steps[self.indices[-1]] = self.steps
        # This path is not better than others, remove it
        elif min_steps[self.indices[-1]] <= self.steps:
            return False

        # Finds list of possible directions path can take
        possible_directions = []
        for dir, offset in enumerate(self.neighbours):
            if self.indices[-1] + offset in obstacles:  # Obstacle in way
                continue
            # If on adding the offset would lead to going over the edge, continue
            if (self.indices[-1] < size[0],
                self.indices[-1] % size[0] == size[0] - 1,
                self.indices[-1] >= size[0] * (size[1] - 1),
                    self.indices[-1] % size[0] == 0)[dir]:
                continue
            possible_directions.append(dir)

        if len(possible_directions) == 0:
            return False    # No possible paths

        new_paths = []
        for dir in possible_directions[:-1]:
            # Create a new path object, copying self
            # Then update the object
            new_path = Path(self.neighbours,
                            list(self.indices), self.steps)
            new_path.steps += 1
            new_path.indices.append(self.indices[-1] +
                                    self.neighbours[dir])
            new_paths.append(new_path)

        # Update self
        self.steps += 1
        self.indices.append(self.indices[-1] +
                            self.neighbours[possible_directions[-1]])
        return new_paths


# CHANGE THESE based on the puzzle question
size = (71, 71)
num_bytes = 1024

# Converts input_text to tuple of indices where bytes fall
fallen_bytes = tuple(int(pos.split(',')[0]) * size[0] + int(pos.split(',')[1])
                     for pos in input_text.split('\n'))

search_paths = [Path((-size[0], 1, size[0], -1), [0], 0)]
solved_paths = []
min_steps = [1e50] * size[0] * size[1]


# Break out if nothing left to search or max_updates reached
while len(search_paths) != 0:
    new_search_paths = []
    for path in search_paths:   # Search through every search path
        new_paths = path.find_next(fallen_bytes[:num_bytes], size, min_steps)

        if new_paths == False:
            search_paths.remove(path)
        elif new_paths == True:         # path is reaches the end
            solved_paths.append(path)   # Add to solved_paths list
            search_paths.remove(path)   # and Remove from search_paths
        else:
            new_search_paths.extend(new_paths)

    search_paths.extend(new_search_paths)

if len(solved_paths) == 0:
    print('No solutions found')
    sys.exit(1)

# Finds lowest steps
min_steps = min(path.steps for path in solved_paths)
print(min_steps)

for num_bytes, fallen_byte in enumerate(fallen_bytes):

    for path in solved_paths:
        if fallen_byte not in path.indices:
            continue
        solved_paths.remove(path)

    if len(solved_paths) > 0:   # There still exists a solution from before
        continue

    # Find new path, initialize values again
    search_paths = [Path((-size[0], 1, size[0], -1), [0], 0)]
    min_steps = [1e50] * size[0] * size[1]

    # Break out if nothing left to search or max_updates reached
    while len(search_paths) != 0:
        new_search_paths = []
        for path in search_paths:   # Search through every search path
            new_paths = path.find_next(
                fallen_bytes[:num_bytes + 1], size, min_steps)

            if new_paths == False:
                search_paths.remove(path)
            elif new_paths == True:         # path is reaches the end
                solved_paths.append(path)   # Add to solved_paths list
                search_paths.remove(path)   # and Remove from search_paths
            else:
                new_search_paths.extend(new_paths)

        search_paths.extend(new_search_paths)

    # No path leads to the end!
    if len(solved_paths) == 0:
        print(f'{fallen_byte//size[0]},{fallen_byte % size[0]}')
        break
