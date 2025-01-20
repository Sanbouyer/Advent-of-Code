# Import input.txt as str
import sys
input_text = open('input.txt').read()


class Path:
    def __init__(self, neighbours: tuple[int], indices: list, direction: int, score: int = 0):
        self.indices = indices
        self.neighbours = neighbours
        self.score = score
        self.direction = direction

    def find_next(self, maze: str, min_scores: list) -> bool | list[object]:
        """Does a generation of the path object, finding the next possible directions it can go and updating its score.

        Args:
            maze (str): The maze to navigate as a string, with '#' as walls and 'E' as the end
            min_scores (list): The smallest score to reach the index.
                               Used to remove least optimal paths without recalculating all future paths from there.

        Returns:
            True: if the end ('E') has been reached
            False: if it is a dead end or the path is not optimal
            list[object]: List containing new path objects spawned from an crossroads
        """
        if maze[self.indices[-1]] == 'E':                       # Reached the end
            return True
        # This path is better, update min_scores
        if min_scores[self.indices[-1]] > self.score:
            min_scores[self.indices[-1]] = self.score
        # This path is not optimal, remove it
        elif min_scores[self.indices[-1]] < self.score - 1000:
            return False

        # Finds list of possible directions path can take
        possible_directions = []
        for dir, offset in enumerate(self.neighbours):
            if dir == (self.direction + 2) % 4:         # Can't go back on itself
                continue
            if maze[self.indices[-1] + offset] == '#':  # Can't go into a wall
                continue
            possible_directions.append(dir)

        if len(possible_directions) == 0:
            return False    # No possible paths

        new_paths = []
        for dir in possible_directions[:-1]:
            # Create a new path object, copying self
            # Then update the object
            new_path = Path(self.neighbours,
                            list(self.indices), dir, self.score)
            new_path.score += (not (dir == self.direction)) * 1000 + 1
            new_path.indices.append(self.indices[-1] +
                                    self.neighbours[dir])
            new_paths.append(new_path)

        # Update self
        self.score += (not (possible_directions[-1]
                       == self.direction)) * 1000 + 1
        self.direction = possible_directions[-1]
        self.indices.append(self.indices[-1] +
                            self.neighbours[possible_directions[-1]])

        return new_paths


width = input_text.find('\n')
maze = input_text.replace('\n', '')

search_paths = [Path((-width, 1, width, -1), [maze.find('S')], 1)]
solved_paths = []
min_scores = [1e50]*len(maze)

max_updates = 1000
# Break out if nothing left to search or max_updates reached
while len(search_paths) != 0 and max_updates > 0:
    new_search_paths = []
    for path in search_paths:   # Search through every search path
        new_paths = path.find_next(maze, min_scores)

        if new_paths == False:
            search_paths.remove(path)
        elif new_paths == True:         # path is reaches the end
            solved_paths.append(path)   # Add to solved_paths list
            search_paths.remove(path)   # and Remove from search_paths
        else:
            new_search_paths.extend(new_paths)

    search_paths.extend(new_search_paths)
    max_updates -= 1

if len(solved_paths) == 0:
    print('No solutions found')
    sys.exit(1)

# Finds lowest score
min_score = min(path.score for path in solved_paths)
print(min_score)

# Finds spots that go along the lowest scoring path
best_spots = set()
for path in solved_paths:
    if path.score == min_score:                 # If the path taken is optimal:
        # Adds the all path.indices to best_spots
        best_spots.update(set(path.indices))

print(len(best_spots))
