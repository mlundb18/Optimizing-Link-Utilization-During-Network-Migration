import sys
sys.path.append('algorithm')
sys.path.append('../experiment_setup/')
import IntegerProgramming as ip
import LinearProgramming as lp
import constants
import multiprocessing

def run_lp_decision(traffic_systems, iterations = constants.LP_ITERATIONS, max_util = 1, scaling = 1, monotonic=False):
    result_list = []
    l = len(traffic_systems)
    task = lp.pulp_update_sequence_decision
    items = zip(traffic_systems, [iterations] * l, [max_util] * l, [scaling] * l, [monotonic] * l)
    with multiprocessing.Pool(constants.MAX_NUMBER_OF_PROCESSES) as pool:
        results = pool.starmap_async(task, items)
        for result in results.get():
            result_list.append(result)
    return result_list

def run_lp_optimization(traffic_systems, iterations = constants.LP_ITERATIONS, scaling = 1, monotonic=False):
    result_list = []
    l = len(traffic_systems)
    task = lp.pulp_update_sequence_optimization
    items = zip(traffic_systems, [iterations] * l, [scaling] * l, [monotonic] * l)
    with multiprocessing.Pool(constants.MAX_NUMBER_OF_PROCESSES) as pool:
        results = pool.starmap_async(task, items)
        for result in results.get():
            result_list.append(result)
    return result_list

def run_mip_decision(traffic_systems, iteration_scaling = constants.MIP_ITERATION_SCALING, max_util = 1, scaling = 1):
    result_strings = []
    results = []
    pool = multiprocessing.Pool(constants.MAX_NUMBER_OF_PROCESSES)
    for traffic_system in traffic_systems:
        iterations = int(len(traffic_system.flows) * iteration_scaling + 1)
        results.append(pool.apply_async(ip.mip_atomic_update_sequence_decision, args=(traffic_system, iterations, max_util, scaling)))
    pool.close()
    pool.join()
    for result in results:
        result_strings.append(result.get())
    return result_strings

def run_mip_optimization(traffic_systems, iteration_scaling = constants.MIP_ITERATION_SCALING, scaling = 1):
    result_strings = []
    results = []
    pool = multiprocessing.Pool(constants.MAX_NUMBER_OF_PROCESSES)
    for traffic_system in traffic_systems:
        iterations = int(len(traffic_system.flows) * iteration_scaling + 1)
        results.append(pool.apply_async(ip.mip_atomic_update_sequence_optimization, args=(traffic_system, iterations, scaling)))
    pool.close()
    pool.join()
    for result in results:
        result_strings.append(result.get())
    return result_strings