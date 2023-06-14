import sys
sys.path.append('parser')
sys.path.append('datatypes')
sys.path.append('generator')

import os
import json
import Datatypes as dt
import random
import Parser as Parser
import networkx as nx
import GravityModel as gm


fileLocationFlows = "data/TopologyZooFlows/Flow10x" #change this to general location and append the file name as needed


def generate_flows(graph, amount_of_flows, demand_range):
    flows = []
    for i in range(amount_of_flows):
        print('\r'+'generating flow ' +str(i+1)+' of '+str(amount_of_flows), end='')

        available_nodes = remove_unconnected_nodes(graph)

        initial_node = random.choice(available_nodes)
        available_final_nodes = connected_nodes(graph, initial_node)
        final_node = random.choice(available_final_nodes)

        initial_node = int(initial_node)
        final_node = int(final_node)

        initial_path = path_find(initial_node, final_node, graph, [initial_node])[0]

        final_node = random.choice(available_final_nodes)
        final_node = int(final_node)

        final_path = path_find(initial_node, final_node, graph, [initial_node], initial_path)[0]

        demand_size = random.randrange(demand_range)+1

        flows.append(dt.Flow(initial_path, final_path, demand_size))
    return flows

def generate_gravity_flows(graph, amount_of_flows):
    flows = []
    for i in range(amount_of_flows):
        print('\r'+'generating flow ' +str(i+1)+' of '+str(amount_of_flows), end='')

        available_nodes = remove_unconnected_nodes(graph)

        initial_node = random.choice(available_nodes)
        available_final_nodes = connected_nodes(graph, initial_node)
        final_node1 = random.choice(available_final_nodes)

        initial_node = int(initial_node)
        final_node1 = int(final_node1)

        initial_path = path_find(initial_node, final_node1, graph, [initial_node])[0]

        final_node2 = random.choice(available_final_nodes)
        final_node2 = int(final_node2)

        final_path = path_find(initial_node, final_node2, graph, [initial_node], initial_path)[0]

        initial_gravity = nx.get_node_attributes(graph, "gravity")[str(initial_node)]
        final_gravity = nx.get_node_attributes(graph, "gravity")[str(final_node1)]

        demand_size = initial_gravity * final_gravity



        flows.append(dt.Flow(convert_node_path_to_edges(initial_path), convert_node_path_to_edges(final_path), demand_size))
    return flows

def convert_node_path_to_edges(path):
    updated_path = []
    previous_node = None

    for node in path:
        if previous_node != None:
            updated_path.append((previous_node, node))
        previous_node = node

    return updated_path

def connected_nodes(graph, initial_node):
    connected_node_list = []
    connected_node_list.append(initial_node)

    checked_nodes = []
    checked_nodes.append(initial_node)

    for nodes in graph.neighbors(initial_node):
        connected_node_list.append(nodes)

    nodes_to_check = (set(connected_node_list) - set(checked_nodes))

    while len(nodes_to_check) != 0:
        nodes_to_check = (set(connected_node_list) - set(checked_nodes))
        for nodes in nodes_to_check:
            checked_nodes.append(nodes)

            for neighbour_nodes in graph.neighbors(nodes):
                if neighbour_nodes not in connected_node_list:
                    connected_node_list.append(neighbour_nodes)
    connected_node_list.remove(initial_node)
    return connected_node_list

def remove_unconnected_nodes(graph):
    all_connected_nodes = []

    for nodes in graph.nodes:
        neighbor_list = []

        for neighbor in graph.neighbors(nodes):
            neighbor_list.append(neighbor)

        if neighbor_list != []:
            all_connected_nodes.append(nodes)

    return all_connected_nodes

def path_find(initial_node, final_node, graph, current_path, test = [None]):
    path = [None]
    temp_keys = []
    checked_nodes = [int(initial_node)]

    if current_path[len(current_path) - 1] == final_node:
        return current_path, checked_nodes
    else:
        for connected_nodes in graph[str(initial_node)]:
            if int(connected_nodes) not in current_path:
                temp_keys.append(int(connected_nodes))
        random.shuffle(temp_keys)

        for nodes in temp_keys:
            temp_path = current_path.copy()
            temp_path.append(nodes)
            if nodes not in checked_nodes:
                path, checked_nodes_temp = path_find(nodes, final_node, graph, temp_path, test)
                checked_nodes += checked_nodes_temp
            if path[len(path) - 1] == final_node:
                if path != test:
                    break

    if path == [None]:
        return test, checked_nodes
    return path, checked_nodes

def save_as_json(flows, topology_name, iteration): #expand this to properly iterate the files and name file correctly
    flow_list = []
    for f in flows:
        flow_list.append((f.initial_path, f.final_path, f.demand))
    json_dict = {'flows': flow_list, 'name': topology_name, 'iteration': iteration}
    json_object = json.dumps(json_dict, indent=4)

    file_output = os.path.join(fileLocationFlows, topology_name + "_" + str(iteration) + ".json")
    os.makedirs(fileLocationFlows, exist_ok=True)
    with open(file_output, "w") as outfile:
        outfile.write(json_object)
    print()
    print("saved flows for " + file_output)
    print()

def generate_flow_dataset(parsed_topologies):
    for topology in parsed_topologies:
        for i in range(1):
            print("generating flows for " + topology.graph['label'] + " on iteration "+str(i+1))
            flows = generate_gravity_flows(gm.set_node_gravity(topology), int(topology.number_of_nodes()*10))
            save_as_json(flows, topology.graph['label'], i+1)

def main():
    generate_flow_dataset(Parser.k_smallest_topologies(260))

if __name__ == "__main__":
    main()