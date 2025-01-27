# Import input.txt as str
with open('input.txt') as input:
    input_text = input.read()


class Region:
    def __init__(self, letter, index, text, width):
        self.letter = letter
        self.indices = set()
        self.indices.add(index)
        self.edges = {}    # Dictionary of each index in region with neighbours outside region
        self.edges[index] = [True] * 4
        self.index_offset = [-width, 1, width, -1]      # ^, >, down, <
        self.text = text
        self.width = width
        self.height = len(text) // width

    def expand_region(self, last_members):
        new_members = set()
        for index in last_members:
            for i, outsider in enumerate(self.index_offset):
                if not self.edges[index][i] or [index//self.width == 0, index % self.width == self.width-1, index//self.width == self.height-1, index % self.width == 0][i]:
                    continue
                if self.text[outsider + index] == self.letter:
                    self.edges[index][i] = False
                    new_members.add(outsider + index)
                    try:
                        self.edges[outsider + index][(i+2) % 4] = False
                    except KeyError:
                        self.edges[outsider + index] = [j !=
                                                        (i+2) % 4 for j in range(4)]
        self.indices.update(new_members)
        return new_members

    def get_score(self, bulk_discount: bool):
        area = len(self.indices)
        if not bulk_discount:
            perimeter = sum(sum(edge)
                            for edge in self.edges.values())
        else:
            perimeter = sum(self.straight_perimeter(index)
                            for index in self.indices) >> 1
            print(perimeter)
        return area * perimeter

    def straight_perimeter(self, index):
        # We want to double count number of outside corners + number of inside corners
        if sum(self.edges[index]) == 0:     # All neighbours -> 0 corners
            return 0
        if sum(self.edges[index]) == 4:     # No neighbours -> 4 outside corners
            return 8

        if sum(self.edges[index]) == 1:     # No outside, 1/2 per inside
            edge = self.edges[index].index(True)

            return sum(not self.edges[index + self.index_offset[(edge + offset[0]) % 4]][(edge + offset[1]) % 4] for offset in ((1, 0), (3, 0)))

        if sum(self.edges[index]) == 3:     # 2 outside, 1/2 per inside
            edge = self.edges[index].index(False)

            return 4 + sum(not self.edges[index + self.index_offset[(edge + offset[0]) % 4]][(edge + offset[1]) % 4] for offset in ((0, 1), (0, 3)))

        # Only 2 left, need to separate between a corner and parrallel
        edge = self.edges[index].index(True)
        if self.edges[index][(edge + 2) % 4]:   # Parrallel case
            return sum(not self.edges[index + self.index_offset[(edge + offset[0]) % 4]][(edge + offset[1]) % 4] for offset in ((1, 0), (3, 0), (1, 2), (3, 2)))
        else:                                   # Corner case
            # Ensure corner is edge and (edge + 1) % 4
            if self.edges[index][(edge-1) % 4]:
                edge = (edge-1) % 4
            return 2 + sum(not self.edges[index + self.index_offset[(edge + offset[0]) % 4]][(edge + offset[1]) % 4] for offset in ((2, 1), (3, 0)))


regions: list[Region] = []

width = input_text.find('\n')
field_str = input_text.replace('\n', '')

for index, letter in enumerate(field_str):
    for region in regions:
        if index in region.indices:
            break
    else:
        new_region = Region(letter, index, field_str, width)
        regions.append(new_region)
        new_members = new_region.expand_region([index])
        while len(new_members):
            new_members = new_region.expand_region(new_members)

print(sum(region.get_score(False) for region in regions))

print(sum(region.get_score(True) for region in regions))
