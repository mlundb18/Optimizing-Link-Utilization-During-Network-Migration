import copy
import sys
sys.path.append('shared_functions')
from nx_additions import on_path
import networkx as nx
import time

def combined_pruning(traffic_system, minimum_threshold = 0):
    traffic_system = copy.deepcopy(traffic_system)
    print('Pruning ' + traffic_system.topology.graph['label'] + '.')
    flows_to_keep = []
    edges_to_remove = []
    threshold = find_prune_threshold(traffic_system, minimum_threshold)
    set_all_edge_traffic_to_zero(traffic_system)
    for flow in traffic_system.flows:
        for edge in list(set(flow.initial_path + flow.final_path)):
            occurrences = max(on_path(edge, flow.initial_path), on_path(edge, flow.final_path))
            capacity = nx.get_edge_attributes(traffic_system.topology, 'capacity')[edge]
            add_edge_traffic(traffic_system, edge, (occurrences * flow.demand) / capacity)
    for flow in traffic_system.flows:
        for edge in list(set(flow.initial_path + flow.final_path)):
            if get_edge_traffic(traffic_system, edge) >= threshold:
                flows_to_keep.append(flow)
                break
    traffic_system.flows = flows_to_keep
    for edge in traffic_system.topology.edges:
        if get_edge_traffic(traffic_system, edge) < threshold:
            edges_to_remove.append(edge)
    for edge in edges_to_remove:
        traffic_system.topology.remove_edge(edge[0], edge[1])
    return traffic_system

def prune_trivial_flows_under_threshold(traffic_system, minimum_threshold = 0):
    traffic_system = copy.deepcopy(traffic_system)
    flows_to_keep = []
    threshold = find_prune_threshold(traffic_system, minimum_threshold)
    set_all_edge_traffic_to_zero(traffic_system)
    for flow in traffic_system.flows:
        for edge in list(set(flow.initial_path + flow.final_path)):
            occurrences = max(on_path(edge, flow.initial_path), on_path(edge, flow.final_path))
            capacity = nx.get_edge_attributes(traffic_system.topology, 'capacity')[edge]
            add_edge_traffic(traffic_system, edge, (occurrences * flow.demand) / capacity)
    for flow in traffic_system.flows:
        for edge in list(set(flow.initial_path + flow.final_path)):
            if get_edge_traffic(traffic_system, edge) >= threshold:
                flows_to_keep.append(flow)
                break
    traffic_system.flows = flows_to_keep
    return traffic_system

def prune_edges_under_threshold(traffic_system, minimum_threshold = 0):
    traffic_system = copy.deepcopy(traffic_system)
    clock = time.perf_counter()
    threshold = find_prune_threshold(traffic_system, minimum_threshold)
    set_all_edge_traffic_to_zero(traffic_system)
    clock = time.perf_counter()
    for flow in traffic_system.flows:
        for edge in list(set(flow.initial_path + flow.final_path)):
            occurrences = max(on_path(edge, flow.initial_path), on_path(edge, flow.final_path))
            capacity = nx.get_edge_attributes(traffic_system.topology, 'capacity')[edge]
            add_edge_traffic(traffic_system, edge, (occurrences * flow.demand) / capacity)
    edges_to_remove = []
    for edge in traffic_system.topology.edges:
        if get_edge_traffic(traffic_system, edge) < threshold:
            edges_to_remove.append(edge)
    for edge in edges_to_remove:
        traffic_system.topology.remove_edge(edge[0], edge[1])
    return traffic_system

def find_prune_threshold(traffic_system, minimum_threshold = 0):
    traffic_system = copy.deepcopy(traffic_system)
    threshold = minimum_threshold
    set_all_edge_traffic_to_zero(traffic_system)
    for flow in traffic_system.flows:
        for edge in flow.initial_path:
            add_edge_traffic(traffic_system, edge, flow.demand / nx.get_edge_attributes(traffic_system.topology, 'capacity')[edge])
    for edge in traffic_system.topology.edges:
        if get_edge_traffic(traffic_system, edge) > threshold:
            threshold = get_edge_traffic(traffic_system, edge)
    set_all_edge_traffic_to_zero(traffic_system)
    for flow in traffic_system.flows:
        for edge in flow.final_path:
            add_edge_traffic(traffic_system, edge, flow.demand / nx.get_edge_attributes(traffic_system.topology, 'capacity')[edge])
    for edge in traffic_system.topology.edges:
        if get_edge_traffic(traffic_system, edge) > threshold:
            threshold = get_edge_traffic(traffic_system, edge)
    return threshold

def set_all_edge_traffic_to_zero(traffic_system):
    for edge in traffic_system.topology.edges:
        set_edge_traffic(traffic_system, edge, 0)

def set_edge_traffic(traffic_system, edge, k):
    if traffic_system.topology.has_edge(edge[0], edge[1]):
        nx.set_edge_attributes(traffic_system.topology, {edge: {'traffic': k}})

def get_edge_traffic(traffic_system, edge):
    if traffic_system.topology.has_edge(edge[0], edge[1]):
        return nx.get_edge_attributes(traffic_system.topology, 'traffic')[edge]

def add_edge_traffic(traffic_system, edge, k):
    if traffic_system.topology.has_edge(edge[0], edge[1]):
        nx.set_edge_attributes(traffic_system.topology, {edge: {'traffic': k + get_edge_traffic(traffic_system, edge)}})