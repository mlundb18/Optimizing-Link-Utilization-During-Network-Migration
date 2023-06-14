import networkx as nx

def test_graph():
    G = nx.Graph()

    G.add_node("0")
    G.add_node("1")
    G.add_node("2")
    G.add_node("3")
    G.add_node("4")

    G.add_edge("0", "1")
    G.add_edge("0", "2")
    G.add_edge("0", "3")
    G.add_edge("0", "4")

    G.add_edge("1", "2")
    G.add_edge("1", "3")
    G.add_edge("1", "4")

    G.add_edge("2", "3")
    G.add_edge("2", "4")

    G.add_edge("3", "4")

    return G

def main():
    print(test_graph())

if __name__ == "__main__":
    main()