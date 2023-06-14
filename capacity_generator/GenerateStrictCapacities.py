import sys
sys.path.append('parser')
import networkx as nx
import common
import os
import Parser as Parser
import copy

strict_cap_file_location = "data/TopologyZooCapacity/strict"
#test = "data/Test"

def allocate_capacity_strict(graph, list_of_flows):
    for edges in graph.edges:
        initial_edge_capacity, final_edge_capacity = common.get_edge_capacities(edges, list_of_flows)

        if initial_edge_capacity > final_edge_capacity:
            nx.set_edge_attributes(graph, {edges: {"capacity": initial_edge_capacity + 1}})
        else:
            nx.set_edge_attributes(graph, {edges: {"capacity": final_edge_capacity + 1}})


    return graph

def generate_topologies_with_strict_capacity(traffic_systems):
    iteration = 1
    name_of_last_seen_traffic_system = ''
    for traffic_system in traffic_systems:
        if traffic_system.topology.graph['label'] == name_of_last_seen_traffic_system:
            iteration += 1
        else:
            iteration = 1
        name_of_last_seen_traffic_system = traffic_system.topology.graph['label']

        new_traffic_system = copy.deepcopy(traffic_system)
        new_traffic_system.topology.graph['label'] += '_' + str(iteration)
        graph_with_capacity = allocate_capacity_strict(new_traffic_system.topology, traffic_system.flows)
        file_name = new_traffic_system.topology.graph['label']
        file_destination = os.path.join(strict_cap_file_location, (file_name + ".graphml"))
        nx.write_graphml(graph_with_capacity, file_destination)
        print('Successfully generated strict capacity for network ' + new_traffic_system.topology.graph['label'])

def main():
    generate_topologies_with_strict_capacity(Parser.generate_traffic_systems(Parser.parse_flows(), Parser.parse_zoo_topologies()))

if __name__ == "__main__":
    main()