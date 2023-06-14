import sys
sys.path.append('preprocessor')
sys.path.append('shared_functions')
sys.path.append('./')
import networkx as nx
import Preprocessor as Preprocessor
import mip
from nx_additions import on_path
import os
import json
import time
import constants

logdir = 'logs/'

def mip_atomic_update_sequence_decision(traffic_system, iterations, max_util = 1, scaling = 1):
    model = mip.Model()
    alpha = model.add_var(name='alpha', var_type='CONTINUOUS', lb=0)
    x = [[model.add_var(name='x '+str(i)+' '+str(flow),var_type='CONTINUOUS', lb=0, ub=1) for flow in range(len(traffic_system.flows))] for i in range(iterations)]
    y = [[model.add_var(name='y '+str(i)+' '+str(flow),var_type='BINARY') for flow in range(len(traffic_system.flows))] for i in range(iterations)]

    capacity = nx.get_edge_attributes(traffic_system.topology, 'capacity')
    edge_temp_load = nx.get_edge_attributes(traffic_system.topology, 'temp_load')

    model += alpha <= max_util

    for i in range(iterations):
        for e in traffic_system.topology.edges:
            model += alpha >= mip.xsum((((1 - x[i][flow]) * on_path(e,traffic_system.flows[flow].initial_path) + x[i][flow] * on_path(e,traffic_system.flows[flow].final_path)) * traffic_system.flows[flow].demand * scaling) / capacity[e] for flow in range(len(traffic_system.flows))) + edge_temp_load[e] / capacity[e]

    for i in range(iterations - 1):
        for j in range(len(x[i])):
            model += -y[i][j] <= x[i][j] - x[i+1][j]
            model += x[i][j] - x[i+1][j] <= y[i][j]

    for i in range(iterations):
        model += mip.xsum(y_var for y_var in y[i]) <= 1

    for j in x[0]:
        model += j == 0

    for j in x[iterations - 1]:
        model += j == 1

    model.verbose = 0
    start = time.perf_counter()
    model.optimize(max_seconds=constants.TIMELIMIT)
    total = time.perf_counter() - start
    timeout = False
    if total >= constants.TIMELIMIT:
        timeout = True

    status = ''
    if model.status == mip.OptimizationStatus.OPTIMAL:
        status += 'feasible'
    elif model.status == mip.OptimizationStatus.INFEASIBLE:
        status += 'infeasible'
    else:
        status += 'error'


    result_json = {'status': status, 'label':traffic_system.topology.graph['label'],
                   'solve_time': total, 'node_count': len(traffic_system.topology.nodes),
                   'edge_count': len(traffic_system.topology.edges),
                   'flow_count': len(traffic_system.flows), 'timeout': timeout}

    return result_json


def mip_atomic_update_sequence_optimization(traffic_system, iterations, scaling = 1):
    model = mip.Model()
    alpha = model.add_var(name='alpha', var_type='CONTINUOUS', lb=0)
    x = [[model.add_var(name='x '+str(i)+' '+str(flow),var_type='CONTINUOUS', lb=0, ub=1) for flow in range(len(traffic_system.flows))] for i in range(iterations)]
    y = [[model.add_var(name='y '+str(i)+' '+str(flow),var_type='BINARY') for flow in range(len(traffic_system.flows))] for i in range(iterations)]
    model.objective = mip.minimize(alpha)

    capacity = nx.get_edge_attributes(traffic_system.topology, 'capacity')
    edge_temp_load = nx.get_edge_attributes(traffic_system.topology, 'temp_load')

    for i in range(iterations):
        for e in traffic_system.topology.edges:
            model += alpha >= mip.xsum((((1 - x[i][flow]) * on_path(e,traffic_system.flows[flow].initial_path) + x[i][flow] * on_path(e,traffic_system.flows[flow].final_path)) * traffic_system.flows[flow].demand * scaling) / capacity[e] for flow in range(len(traffic_system.flows))) + edge_temp_load[e] / capacity[e]

    for i in range(iterations - 1):
        for j in range(len(x[i])):
            model += -y[i][j] <= x[i][j] - x[i+1][j]
            model += x[i][j] - x[i+1][j] <= y[i][j]

    for i in range(iterations):
        model += mip.xsum(y_var for y_var in y[i]) <= 1

    for j in x[0]:
        model += j == 0

    for j in x[iterations - 1]:
        model += j == 1

    model.verbose = 0
    start = time.perf_counter()
    model.optimize(max_seconds=constants.TIMELIMIT)
    total = time.perf_counter() - start

    timeout = False
    if total >= constants.TIMELIMIT:
        timeout = True

    result_json = {'alpha': model.objective_value, 'label':traffic_system.topology.graph['label'],
                   'solve_time': total, 'node_count': len(traffic_system.topology.nodes),
                   'edge_count': len(traffic_system.topology.edges), 'flow_count': len(traffic_system.flows),
                   'timeout': timeout}

    return result_json

def main():
    ''


if __name__ == "__main__":
    main()