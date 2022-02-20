from importlib import import_module
import unittest
import networkx as nx
from movement import create_graph

def test_create_graph():
    # G = nx.DiGraph()
    # G.add_edge(1, 2)
    # G.add_edge(2, 1)
    # for edge in G.edges(data=True):
    #     if edge[0] == 1:
    #         print("found1")
    #         print(edge[1])
    #     if edge[0] == 2:
    #         print("found2")
    #         print(edge[1])
    G = create_graph()
    school_list = []
    for (u,v,e) in [(u,v,e) for u,v,e in G.edges(data=True)]:
        if v == "University of Massachusetts Amherst":
            school_list.append((u,v,e))
    for i in school_list:
        print(i)
test_create_graph()

