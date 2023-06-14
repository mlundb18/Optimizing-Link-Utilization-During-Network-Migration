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

EXPERIMENT_FOLDER = 'trivial_flow_pruning/'

def run():
    traffic_systems = Preprocessor.produce_traffic_systems()
    pruned_traffic_systems = Preprocessor.prune_trivial_flows(traffic_systems)

    pruned_traffic_systems_results_op = run_lp_optimization(pruned_traffic_systems)

    save_results_as_json_files(pruned_traffic_systems_results_op, EXPERIMENT_FOLDER + "optimization/")

def main():
    run()


if __name__ == "__main__":
    main()