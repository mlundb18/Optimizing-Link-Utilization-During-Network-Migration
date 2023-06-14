import networkx as nx

def allocate_capacity_random(graph, list_of_flows, percentage): #fix percentage upto that amount more of capacity
    for edges in graph.edges:
        initial_edge_capacity, final_edge_capacity = get_edge_capacities(edges, list_of_flows)

        if initial_edge_capacity > final_edge_capacity:
            if initial_edge_capacity > 0:
                random_initial_capacity = random.randrange(int(initial_edge_capacity*percentage)+1)
            else:
                random_initial_capacity = 0

            nx.set_edge_attributes(graph, {edges:{"capacity": (initial_edge_capacity+random_initial_capacity)}})
        else:
            if final_edge_capacity > 0:
                random_final_capacity = random.randrange(int(final_edge_capacity * percentage)+1)
            else:
                random_final_capacity = 0

            nx.set_edge_attributes(graph, {edges: {"capacity": (final_edge_capacity+ random_final_capacity)}})

    return graph