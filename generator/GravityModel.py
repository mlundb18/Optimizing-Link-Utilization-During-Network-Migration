import sys
sys.path.append('datatypes')
sys.path.append('parser')

import os
import json
import Datatypes as dt
import random
import Parser as Parser
import networkx as nx

def test_graph():
    G = nx.Graph()

    G.add_node(1)
    G.add_node(2)
    G.add_node(3)
    G.add_node(4)
    G.add_node(5)

    G.add_edge(1, 2)
    G.add_edge(1, 3)
    G.add_edge(1, 4)
    G.add_edge(1, 5)

    G.add_edge(2, 3)
    G.add_edge(2, 4)
    G.add_edge(2, 5)

    G.add_edge(3, 4)
    G.add_edge(3, 5)

    G.add_edge(4, 5)

    return G

def set_node_gravity(graph):

    for nodes in graph.nodes:
        node_gravity = random.randrange(10)+1
        node_gravity = node_gravity*node_gravity
        nx.set_node_attributes(graph, {nodes: {"gravity": node_gravity + 1}})
    return graph

def main():
    print("Hello")
    set_node_gravity(test_graph())

if __name__ == "__main__":
    main()