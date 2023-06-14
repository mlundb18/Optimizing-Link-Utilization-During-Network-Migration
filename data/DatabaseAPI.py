import networkx as nx
import os

flow_file_location = "data/TopologyZooFlows/Flow10x"
topology_file_location = "data/TopologyZoo"
capacity_file_location = "data/CapacitatedTopologyZoo/Generalized"
#logs_file_location = "logs/lp_optimization"
#logs_file_location = "logs/lp_decision"

def get_zoo_topologies():
    return get_files_from_directory(topology_file_location)

def get_zoo_topologies_with_capacity():
    return get_files_from_directory(capacity_file_location)

def get_zoo_flows():
    return get_files_from_directory(flow_file_location)

def get_flows(dataset):
    return get_files_from_directory(dataset)

def get_topologies_with_capacity(dataset):
    return get_files_from_directory(dataset)

def get_files_from_directory(directory):
    files = []
    for filename in os.listdir(directory):
        temp_file = open(os.path.join(directory, filename), "r")
        files.append((temp_file.read(), filename))
        temp_file.close()

    return files

def get_logs_files(logs_file_location):
    return get_files_from_directory(logs_file_location)

def main():
    for flows in get_logs_files():
        print(flows)

if __name__ == "__main__":
    main()