import sys
sys.path.append('shared_functions')
sys.path.append('parser')
sys.path.append('datatypes')
sys.path.append('./')
sys.path.append('preprocessor')
import Parser as Parser
import networkx as nx
import Datatypes as dt
import copy
import multiprocessing
import constants
import time
from nx_additions import on_path
import approximations
import safe_reductions



def produce_traffic_systems(topology_dataset = constants.TOPOLOGY_FILE_LOCATION, flow_dataset = constants.FLOW_FILE_LOCATION):
    traffic_systems = Parser.generate_traffic_systems(Parser.parse_flows(flow_dataset), Parser.parse_zoo_topologies_with_capacity(topology_dataset))
    return traffic_systems

def prune_trivial_flows_and_edges(traffic_systems, minimum_threshold = 0):
    updated_traffic_systems = []
    results = []
    pool = multiprocessing.Pool(constants.MAX_NUMBER_OF_PROCESSES)
    for traffic_system in traffic_systems:
        results.append(
            pool.apply_async(safe_reductions.combined_pruning, args=(traffic_system, minimum_threshold)))
    pool.close()
    pool.join()
    for result in results:
        updated_traffic_systems.append(result.get())
    return updated_traffic_systems

def prune_trivial_flows(traffic_systems, minimum_threshold = 0):
    updated_traffic_systems = []
    results = []
    pool = multiprocessing.Pool(constants.MAX_NUMBER_OF_PROCESSES)
    for traffic_system in traffic_systems:
        results.append(
            pool.apply_async(safe_reductions.prune_trivial_flows_under_threshold, args=(traffic_system, minimum_threshold)))
    pool.close()
    pool.join()
    for result in results:
        updated_traffic_systems.append(result.get())
    return updated_traffic_systems



def prune_trivial_edges(traffic_systems, minimum_threshold = 0):
    updated_traffic_systems = []
    results = []
    pool = multiprocessing.Pool(constants.MAX_NUMBER_OF_PROCESSES)
    for traffic_system in traffic_systems:
        results.append(pool.apply_async(safe_reductions.prune_edges_under_threshold, args=(traffic_system, minimum_threshold)))
    pool.close()
    pool.join()
    for result in results:
        updated_traffic_systems.append(result.get())
    return updated_traffic_systems

def remove_k_percent_smallest_flows(traffic_systems, k):
    updated_traffic_systems = []
    for traffic_system in traffic_systems:
        updated_traffic_systems.append(approximations.remove_k_percent_lowest_flows(traffic_system, k))
    return updated_traffic_systems

def remove_k_percent_of_demand(traffic_systems, k):
    updated_traffic_systems = []
    for traffic_system in traffic_systems:
        updated_traffic_systems.append(approximations.remove_k_percent_demand_of_flows(traffic_system, k))
    return updated_traffic_systems

def main():
    traffic_systems = produce_traffic_systems()

if __name__ == "__main__":
    main()