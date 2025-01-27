import numpy as np
# Import input.txt as str
with open('input.txt') as input:
    input_text = input.read()


def count_regions(robots, middle):
    # This is not the fastest function since it has to loop over every robot, and has lots of clauses
    regions = [0, 0, 0, 0]
    for robot in robots:
        if robot[0] < middle[0] and robot[1] < middle[1]:
            regions[0] += 1
        elif robot[0] < middle[0] and robot[1] > middle[1]:
            regions[1] += 1
        elif robot[0] > middle[0] and robot[1] < middle[1]:
            regions[2] += 1
        elif robot[0] > middle[0] and robot[1] > middle[1]:
            regions[3] += 1
    return regions


def display(robots_initial, time):
    update = np.array((1, time))
    field = np.zeros(grid_size, dtype=int)
    robots_time = np.mod(np.matmul(robots_initial[:], update), grid_size)
    for robot in robots_time:
        field[robot[0], robot[1]] += 1
    field = field.astype(str)
    field[field == '0'] = '.'
    return '\n'.join([''.join(line) for line in field.T])


robots_initial = np.array([np.array(robot.split(','), dtype=int).reshape((2, 2)).T
                          for robot in input_text.replace('p=', '').replace(' v=', ',').split('\n')])

grid_size = np.array((101, 103))
end_time = 100
update = np.array((1, end_time))
robots_time = np.mod(np.matmul(robots_initial[:], update), grid_size)

print(np.prod(count_regions(robots_time, np.floor_divide(grid_size, 2))))

min_deviation = (1000, 0)
for time in range(100000):
    update = np.array((1, time))
    robots_time = np.mod(np.matmul(robots_initial[:], update), grid_size)

    # If it makes an image, the standard deviation will be low, so find the minimum deviation.
    # Random noise would cause a high standard deviation
    deviation = np.std(robots_time, 0)

    if sum(deviation) < min_deviation[0]:
        min_deviation = (sum(deviation), time)

# Show the robots postition to check out the Easter Egg
print(display(robots_initial, min_deviation[1]))

print(min_deviation[1])
