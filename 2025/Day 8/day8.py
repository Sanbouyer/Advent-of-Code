import numpy as np

# Import input.txt as str
with open('input.txt') as input:
    input_text = input.read()

# input_text = """162,817,812
# 57,618,57
# 906,360,560
# 592,479,940
# 352,342,300
# 466,668,158
# 542,29,236
# 431,825,988
# 739,650,466
# 52,470,668
# 216,146,977
# 819,987,18
# 117,168,530
# 805,96,715
# 346,949,466
# 970,615,88
# 941,993,340
# 862,61,35
# 984,92,344
# 425,690,689"""

num_connections = 1000

boxes_str = input_text.split("\n")
num_boxes = len(boxes_str)
boxes = np.zeros((num_boxes, 3))

for i, box in enumerate(boxes_str):
    boxes[i, :] = np.int32(box.split(","))

distances = np.zeros((num_boxes, num_boxes))

for i, box in enumerate(boxes):
    for j, box2 in enumerate(boxes):
        distances[i, j] = np.sum((box-box2)**2, axis=-1)


sorted_dist = np.sort(distances, axis=None)

connected: list[set] = []
i = 0
while True:
    connection = tuple(np.nonzero(
        distances == sorted_dist[num_boxes + 2*i])[0])
    for j, group in enumerate(connected):
        if connection[0] in group:
            group.add(connection[1])
            for group2 in connected:
                if connection[1] in group2 and group2 != group:
                    connected[j] = group.union(group2)
                    connected.remove(group2)
        elif connection[1] in group:
            group.add(connection[0])
            for group2 in connected:
                if connection[0] in group2 and group2 != group:
                    connected[j] = group.union(group2)
                    connected.remove(group2)
        else:
            continue
        break
    else:
        connected.append(set(connection))

    i += 1

    if i == num_connections:
        # Do part 1
        connection_sizes = [len(group) for group in connected]
        connection_sizes.sort(reverse=True)
        print(connection_sizes[0]*connection_sizes[1]*connection_sizes[2])

    if len(connected[0]) == num_boxes:
        # All connected do part 2!
        print(int(boxes[connection[0], 0] * boxes[connection[1], 0]))
        break
