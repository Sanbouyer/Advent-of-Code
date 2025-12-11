import networkx as nx
import matplotlib.pyplot as plt

# Import input.txt as str
with open('input.txt') as input:
    input_text = input.read()

# input_text = """aaa: you hhh
# you: bbb ccc
# bbb: ddd eee
# ccc: ddd eee fff
# ddd: ggg
# eee: out
# fff: out
# ggg: out
# hhh: ccc fff iii
# iii: out"""

# input_text = """svr: aaa bbb
# aaa: fft
# fft: ccc
# bbb: tty
# tty: ccc
# ccc: ddd eee
# ddd: hub
# hub: fff
# eee: dac
# dac: fff
# fff: ggg hhh
# ggg: out
# hhh: out"""

network = nx.DiGraph()
devices = input_text.split("\n")
for device in devices:
    parts = device.split(" ")
    edges = ((parts[0][:-1], output) for output in parts[1:])
    network.add_edges_from(edges)

paths = nx.all_simple_paths(network, "you", "out")
print(sum(1 for dummy in paths))

net1 = network.subgraph(nx.ancestors(network, "fft").union({"fft"}))
net2 = network.subgraph(nx.descendants(
    network, "fft").intersection(nx.ancestors(network, "dac")).union({"fft", "dac"}))
net3 = network.subgraph(nx.descendants(network, "dac").union({"dac"}))

paths_fft = nx.all_simple_paths(net1, "svr", "fft")
paths_fft_dac = nx.all_simple_paths(net2, "fft", "dac")
end_paths_dac = nx.all_simple_paths(net3, "dac", "out")

# Print these since it takes a long time to run
n3 = sum(1 for dummy in end_paths_dac)
print(n3)
n1 = sum(1 for dummy in paths_fft)
print(n1)
# This final one takes a very long time to run, there are 4368408 paths!
n2 = sum(1 for dummy in paths_fft_dac)
print(n2)

print(n1 * n2 * n3)


# Plot graph for visual
for node in network.nodes(True):
    if node[0] in ("svr", "fft", "dac", "out"):
        node[1]["c"] = "r"
    else:
        node[1]["c"] = "c"
    dist_svr = nx.shortest_path_length(network, "svr", node[0])
    node[1]["dist"] = dist_svr

colours = dict(network.nodes.data("c")).values()

nx.draw(network, pos=nx.multipartite_layout(network, subset_key="dist"),
        with_labels=True, node_color=colours)

plt.show()
