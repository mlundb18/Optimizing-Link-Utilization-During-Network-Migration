import sys

import constants

sys.path.append('preprocessor')
sys.path.append('shared_functions')
sys.path.append('./')
import networkx as nx
import Preprocessor as Preprocessor
from nx_additions import on_path
import pulp
import json
import time
import os
import constants

logdir = 'logs/'

def parse_problem_to_integer_programming():

    return

def pulp_update_sequence_decision(traffic_system, iterations = constants.LP_ITERATIONS, max_util = 1, scaling = 1, monotonic = False):
    capacity = nx.get_edge_attributes(traffic_system.topology, 'capacity')
    temp_load = nx.get_edge_attributes(traffic_system.topology, 'temp_load')
    edge_capacities = []
    edge_temp_load = []
    on_path_list_initial = []
    on_path_list_final = []
    num = 0
    for e in traffic_system.topology.edges:
        edge_capacities.append(capacity[e])
        edge_temp_load.append(temp_load[e])
        on_path_list_initial.append([])
        on_path_list_final.append([])
        for flow in range(len(traffic_system.flows)):
            on_path_list_initial[num].append(on_path(e, traffic_system.flows[flow].initial_path))
            on_path_list_final[num].append(on_path(e, traffic_system.flows[flow].final_path))
        num += 1

    model = pulp.LpProblem("General_Update_Sequence_Decision_Problem", pulp.LpMinimize)
    alpha = pulp.LpVariable("alpha", 0)
    x = [[pulp.LpVariable("x" + str(i) + "," + str(flow), 0, 1, pulp.LpContinuous) for flow in range(len(traffic_system.flows))] for i in range(iterations)]
    y = [[[pulp.LpVariable("y" + str(e) + "," + str(i) + "," + str(flow), 0, None, pulp.LpContinuous) for flow in range(len(traffic_system.flows))] for i in range(iterations - 1)] for e in range(len(traffic_system.topology.edges))]

    #Objective function
    model += 0

    model += alpha <= max_util

    for e in range(len(traffic_system.topology.edges)):
        for i in range(iterations - 1):
            model += (alpha >= pulp.lpSum(y[e][i][flow] for flow in range(len(traffic_system.flows))) + edge_temp_load[e] / edge_capacities[e], "y_sum" + str(e) + "," + str(i))

    for flow in range(len(traffic_system.flows)):
        model += x[0][flow] == 0, "x" + str(0) + "," + str(flow) + "=0"
        model += x[iterations - 1][flow] == 1, "x" + str(iterations - 1) + "," + str(flow) + "=1"

    for e in range(len(traffic_system.topology.edges)):
        for i in range(iterations - 1):
            for flow in range(len(traffic_system.flows)):
                model += y[e][i][flow] >= (((1 - x[i][flow]) * on_path_list_initial[e][flow] + x[i][flow] * on_path_list_final[e][flow]) * traffic_system.flows[flow].demand * scaling) / edge_capacities[e], "y" + str(e) + "," + str(i) + "," + str(flow) + "-load0"
                model += y[e][i][flow] >= (((1 - x[i + 1][flow]) * on_path_list_initial[e][flow] + x[i + 1][flow] * on_path_list_final[e][flow]) * traffic_system.flows[flow].demand * scaling) / edge_capacities[e], "y" + str(e) + "," + str(i) + "," + str(flow) + "-load1"

    if monotonic:
        for i in range(iterations - 1):
            for flow in range(len(traffic_system.flows)):
                model += x[i][flow] <= x[i+1][flow]

    start = time.perf_counter()
    model.solve(pulp.PULP_CBC_CMD(timeLimit=constants.TIMELIMIT, msg=False))
    total = time.perf_counter() - start

    timeout = False
    if total >= constants.TIMELIMIT:
        timeout = True

    status = ''
    if model.status == 1:
        status += 'feasible'
    elif model.status == -1:
        status += 'infeasible'
    else:
        status += 'error'

    result_json = { 'status':status, 'label':traffic_system.topology.graph['label'],
                    'solve_time':total, 'node_count':len(traffic_system.topology.nodes),
                    'edge_count':len(traffic_system.topology.edges),
                    'flow_count':len(traffic_system.flows), 'timeout':timeout }
    return result_json

def pulp_update_sequence_optimization(traffic_system, iterations = constants.LP_ITERATIONS, scaling = 1, monotonic = False):
    capacity = nx.get_edge_attributes(traffic_system.topology, 'capacity')
    temp_load = nx.get_edge_attributes(traffic_system.topology, 'temp_load')
    edge_capacities = []
    edge_temp_load = []
    on_path_list_initial = []
    on_path_list_final = []
    num = 0
    for e in traffic_system.topology.edges:
        edge_capacities.append(capacity[e])
        edge_temp_load.append(temp_load[e])
        on_path_list_initial.append([])
        on_path_list_final.append([])
        for flow in range(len(traffic_system.flows)):
            on_path_list_initial[num].append(on_path(e, traffic_system.flows[flow].initial_path))
            on_path_list_final[num].append(on_path(e, traffic_system.flows[flow].final_path))
        num += 1

    model = pulp.LpProblem("General_Update_Sequence_Decision_Problem", pulp.LpMinimize)
    alpha = pulp.LpVariable("alpha", 0)
    x = [[pulp.LpVariable("x" + str(i) + "," + str(flow), 0, 1, pulp.LpContinuous) for flow in range(len(traffic_system.flows))] for i in range(iterations)]
    y = [[[pulp.LpVariable("y" + str(e) + "," + str(i) + "," + str(flow), 0, None, pulp.LpContinuous) for flow in range(len(traffic_system.flows))] for i in range(iterations - 1)] for e in range(len(traffic_system.topology.edges))]

    #Objective function
    model += alpha

    for e in range(len(traffic_system.topology.edges)):
        for i in range(iterations - 1):
            model += (alpha >= pulp.lpSum(y[e][i][flow] for flow in range(len(traffic_system.flows))) + edge_temp_load[e] / edge_capacities[e], "y_sum" + str(e) + "," + str(i))

    for flow in range(len(traffic_system.flows)):
        model += x[0][flow] == 0, "x" + str(0) + "," + str(flow) + "=0"
        model += x[iterations - 1][flow] == 1, "x" + str(iterations - 1) + "," + str(flow) + "=1"

    for e in range(len(traffic_system.topology.edges)):
        for i in range(iterations - 1):
            for flow in range(len(traffic_system.flows)):
                model += y[e][i][flow] >= (((1 - x[i][flow]) * on_path_list_initial[e][flow] + x[i][flow] * on_path_list_final[e][flow]) * traffic_system.flows[flow].demand * scaling) / edge_capacities[e], "y" + str(e) + "," + str(i) + "," + str(flow) + "-load0"
                model += y[e][i][flow] >= (((1 - x[i + 1][flow]) * on_path_list_initial[e][flow] + x[i + 1][flow] * on_path_list_final[e][flow]) * traffic_system.flows[flow].demand * scaling) / edge_capacities[e], "y" + str(e) + "," + str(i) + "," + str(flow) + "-load1"

    if monotonic:
        for i in range(iterations - 1):
            for flow in range(len(traffic_system.flows)):
                model += x[i][flow] <= x[i+1][flow]

    start = time.perf_counter()
    model.solve(pulp.PULP_CBC_CMD(timeLimit=constants.TIMELIMIT, msg=False))
    total = time.perf_counter() - start

    timeout = False
    if total >= constants.TIMELIMIT:
        timeout = True

    results = { 'alpha':model.variables()[0].varValue, 'label':traffic_system.topology.graph['label'],
                'solve_time':total, 'node_count':len(traffic_system.topology.nodes),
                'edge_count':len(traffic_system.topology.edges),
                'flow_count':len(traffic_system.flows), 'timeout':timeout}

    print("topology solved")

    return results



def main():
    #graph = nx.Graph()
    #graph.add_node("0")
    #graph.add_node("1")
    #graph.add_node("2")
    #graph.add_edge("0", "1", capacity=1)
    #graph.add_edge("0", "2", capacity=1)
    #graph.add_edge("1", "2", capacity=1)
    #flow1 = dt.Flow([0, 2], [0, 1, 2], 1)
    #flow2 = dt.Flow([0, 1, 2], [0, 2], 1)
    #pulp_update_sequence(dt.TrafficSystem([flow1, flow2], graph), 7, 1)

    traffic_systems = Preprocessor.produce_traffic_systems()
    for traffic_system in traffic_systems:
        pulp_update_sequence_optimization(traffic_system, 10)


if __name__ == "__main__":
    main()