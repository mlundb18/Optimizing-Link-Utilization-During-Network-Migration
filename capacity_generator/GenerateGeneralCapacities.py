import sys
sys.path.append('parser')
import networkx as nx
import common
import os
import Parser as Parser
import copy

general_cap_directory = "data/CapacitatedTopologyZoo/Generalized/"

def allocate_capacity_generalized(graph):
    normal_graph = nx.Graph(graph)
    digraph_copy = normal_graph.to_directed()
    for edges in digraph_copy.edges:
        nx.set_edge_attributes(digraph_copy, {edges: {"capacity": 100000}})
        nx.set_edge_attributes(digraph_copy, {edges: {"temp_load": 0}})

    return digraph_copy

def generate_topologies_with_generalized_capacity(traffic_systems):
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
        graph_with_capacity = allocate_capacity_generalized(new_traffic_system.topology)
        file_name = new_traffic_system.topology.graph['label']
        file_destination = os.path.join(general_cap_directory, (file_name + ".graphml"))
        os.makedirs(general_cap_directory, exist_ok=True)
        nx.write_graphml(graph_with_capacity, file_destination)
        print('Successfully generated strict capacity for network ' + new_traffic_system.topology.graph['label'])

def main():
    generate_topologies_with_generalized_capacity(Parser.generate_traffic_systems(Parser.parse_flows(), Parser.parse_zoo_topologies()))

if __name__ == "__main__":
    main()