import itertools
import os, csv
import networkx as nx
from networkx.algorithms import community
G = nx.path_graph(8)
k = 3
comp = community.girvan_newman(G)
print(type(comp))
for it in comp:
    print(tuple(sorted(c) for c in it))
    # for com in tuple(sorted(c) for c in it):
    #     print(com)
comp = community.girvan_newman(G)
limited = itertools.takewhile(lambda c: len(c) <= k, comp)
print("###########")
print(type(limited))
for communities in limited:
    print(tuple(sorted(c) for c in communities))