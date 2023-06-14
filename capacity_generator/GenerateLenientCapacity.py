import networkx as nx

def allocate_capacity_lenient(graph, list_of_flows, percentage): #fix percentage strictly that much more capacity
    for edges in graph.edges:
        initial_edge_capacity, final_edge_capacity = get_edge_capacities(edges, list_of_flows)

        if initial_edge_capacity > final_edge_capacity:
            nx.set_edge_attributes(graph, {edges:{"capacity": (initial_edge_capacity + int(initial_edge_capacity * percentage))}})
        else:
            nx.set_edge_attributes(graph, {edges: {"capacity": (final_edge_capacity + int(final_edge_capacity * percentage))}})

    return graph