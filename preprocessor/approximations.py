import copy
import sys
sys.path.append('shared_functions')
from nx_additions import on_path
from nx_additions import has_edge
import networkx as nx

def k_lowest_flows_traffic_system(traffic_systems, k):
    updated_traffic_systems = []
    for ts in traffic_systems:
        updated_traffic_systems.append(remove_k_percent_lowest_flows(ts, k))
    return updated_traffic_systems

def remove_k_percent_lowest_flows(traffic_system, k):
    traffic_system = copy.deepcopy(traffic_system)
    traffic_system.flows = sorted(traffic_system.flows, key=lambda x: x.demand)
    flows_to_remove = int(len(traffic_system.flows) * k)

    templist = traffic_system.flows[0:flows_to_remove]

    traffic_system = add_temp_load(traffic_system, templist)
    traffic_system.flows = traffic_system.flows[flows_to_remove:]

    return traffic_system

def k_percent_demand_traffic_system(traffic_systems, k):
    updated_traffic_systems = []
    for ts in traffic_systems:
        updated_traffic_systems.append(remove_k_percent_demand_of_flows(ts, k))
    return updated_traffic_systems

def remove_k_percent_demand_of_flows(traffic_system, k):
    traffic_system = copy.deepcopy(traffic_system)
    flows_to_remove = []
    flow_removed = 0
    total_demand = 0
    traffic_system.flows = sorted(traffic_system.flows, key=lambda x: x.demand)
    for flow in traffic_system.flows:
        total_demand += flow.demand
    demand_to_remove = total_demand * k
    for flow in traffic_system.flows:
        if flow.demand <= demand_to_remove:
            flows_to_remove.append(flow)
            flow_removed += flow.demand
            demand_to_remove -= flow.demand
    traffic_system = add_temp_load(traffic_system, flows_to_remove)
    traffic_system.flows = traffic_system.flows[len(flows_to_remove):]
    return traffic_system

def add_temp_load(traffic_system, flows):
    for edge in traffic_system.topology.edges:
        temp_edge_load = nx.get_edge_attributes(traffic_system.topology, 'temp_load')[edge]

        for flow in flows:
            if has_edge(edge, flow.initial_path) or has_edge(edge, flow.final_path):
                temp_edge_load = temp_edge_load + flow.demand

        nx.set_edge_attributes(traffic_system.topology, {edge: {'temp_load': temp_edge_load}})
    return traffic_system