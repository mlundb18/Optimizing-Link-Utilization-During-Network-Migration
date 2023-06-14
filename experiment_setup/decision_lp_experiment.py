import sys
sys.path.append('algorithm')
sys.path.append('preprocessor')
sys.path.append('./')
import IntegerProgramming
import LinearProgramming
import Preprocessor
from result_handler import save_results_as_json_files
from run_algorithms import run_lp_optimization
from run_algorithms import run_lp_decision

EXPERIMENT_FOLDER = 'x_demand_scaling/'

def run():
    traffic_systems = Preprocessor.produce_traffic_systems(topology_dataset = 'data/DecisionTestTopologies/', flow_dataset = 'data/DecisionTestFlows/')

    for i in range(1, 41):
        demand_scaling_op = run_lp_optimization(traffic_systems, scaling=i * 0.05)
        save_results_as_json_files(demand_scaling_op, str(i * 0.05) + EXPERIMENT_FOLDER + "optimization/")

        demand_scaling_de = run_lp_decision(traffic_systems, scaling=i * 0.05)
        save_results_as_json_files(demand_scaling_de, str(i * 0.05) + EXPERIMENT_FOLDER + "decision/")

def main():
    run()

if __name__ == "__main__":
    main()