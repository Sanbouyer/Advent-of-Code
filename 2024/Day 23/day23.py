import networkx as nx

# Import input.txt as str
with open('input.txt') as input:
    input_text = input.read()

# Use graphs to solve this problem
network = nx.Graph()
edges = (tuple(link.split('-')) for link in input_text.split('\n'))
network.add_edges_from(edges)

# What we are looking for are called cliques
# Iterate over each and find if it matches the conditions
num_of_t = 0
for clique in nx.enumerate_all_cliques(network):
    if len(clique) != 3:    # Look for 3 interconnected ports -> len(clique) == 3
        continue
    for port in clique:     # For each port in the clique
        if port[0] == 't':  # If it starts with 't' the Chief Historian might be there
            num_of_t += 1
            break           # Break so we don't double count cliques with multiple ports starting with 't'
print(num_of_t)

# nx.find_cliques finds the maximal sized cliques, we then use max to find maximum sized clique
m = max(nx.find_cliques(network), key=len)
m.sort()    # Sort it by alphabet
print(','.join(m))
