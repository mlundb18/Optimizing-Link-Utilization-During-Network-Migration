

def get_edge_capacities(edge, list_of_flows): #move condition check for final or initial capacity to here
    initial_edge_capacity = 0
    final_edge_capacity = 0
    for flow in list_of_flows:
        initial_edge_capacity += aggregate_edge_capacity(flow, edge, flow.initial_path)
        final_edge_capacity += aggregate_edge_capacity(flow, edge, flow.final_path)
    return initial_edge_capacity, final_edge_capacity

def aggregate_edge_capacity(flows, edge, path):#node in path returns a list of nodes, but if it is not properly ordered then issues arrise
    edge_capacity = 0
    previous_node = None
    edge_tuple = (edge[0], edge[1])

    for node in path:
        if previous_node == None:
            previous_node = node

        if edge_tuple == (str(previous_node), str(node)) or edge_tuple == (str(node), str(previous_node)):
            edge_capacity += flows.demand

        previous_node = node

    return edge_capacity

