import sys
sys.path.append("data")
sys.path.append("datatypes")
import networkx as nx
import DatabaseAPI as db
import Datatypes as dt
import random
import json

def parse_zoo_topologies():
    parsed_topologies=[]
    for topology in db.get_zoo_topologies():
        parsed_topologies.append(nx.parse_graphml(topology[0]))
    return parsed_topologies

def parse_zoo_topologies_with_capacity(dataset):
    parsed_topologies = []
    for topologies in db.get_topologies_with_capacity(dataset):
        parsed_topologies.append(nx.parse_graphml(topologies[0]))
    return parsed_topologies


def k_random_topologies(k):
    return random.sample(parse_zoo_topologies(), k)

def k_largest_topologies(k):
    sortedL = sorted(parse_zoo_topologies(), key=lambda x: x.number_of_nodes(), reverse=True)
    return sortedL[0:k]

def k_smallest_topologies(k):
    sortedL = sorted(parse_zoo_topologies(), key=lambda x: x.number_of_nodes(), reverse=True)
    return sortedL[len(sortedL)-k:]

def parse_flows(dataset): #Returns a list of sets of flows. Each set of flows is a tuple with a list of flows and a name
    list_of_flow_sets=[]
    for file_raw in db.get_flows(dataset):
        file_json = json.loads(file_raw[0])
        flow_name = file_json['name']
        flow_iteration = file_json['iteration']
        list_of_flow_sets.append((parse_flow_set(file_json['flows']), flow_name, flow_iteration))
    return list_of_flow_sets

def parse_flow_set(json_flow_list):
    parsed_flows = []
    for json_flow in json_flow_list:
        initial_path = json_flow[0]
        final_path = json_flow[1]
        demand = json_flow[2]
        for i in range(len(initial_path)):
            initial_path[i][0] = str(initial_path[i][0])
            initial_path[i][1] = str(initial_path[i][1])
            initial_path[i] = tuple(initial_path[i])
        for i in range(len(final_path)):
            final_path[i][0] = str(final_path[i][0])
            final_path[i][1] = str(final_path[i][1])
            final_path[i] = tuple(final_path[i])
        parsed_flows.append(dt.Flow(initial_path, final_path, demand))
    return parsed_flows

def generate_traffic_systems(list_of_flow_sets, topology_list):
    traffic_systems = []
    for topology in topology_list:
        for flow_set in list_of_flow_sets:
            if flow_set[1] == topology.graph['label'] or flow_set[1] + '_' + str(flow_set[2]) == topology.graph['label']:
                traffic_systems.append(dt.TrafficSystem(flow_set[0], topology))
    return traffic_systems

def parse_logs():
    raw_logs = db.get_logs_files()
    list_of_logs = []

    for file_raw in raw_logs:
        file_json = json.loads(file_raw[0])
        #file_name = file_json['name']
        list_of_logs.append(file_json)

    return list_of_logs


def main():
    #testlist = generate_traffic_systems(parse_flows(), parse_zoo_topologies_with_strict_capacity())
    testlist = k_smallest_topologies(250)
    for topologies in testlist:
        print(topologies)
        print()


if __name__ == "__main__":
    main()