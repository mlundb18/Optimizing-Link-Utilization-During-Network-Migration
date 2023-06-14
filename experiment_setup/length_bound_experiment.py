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

EXPERIMENT_FOLDER = 'x_iterations/'

def run():
    traffic_systems = Preprocessor.produce_traffic_systems()
    for i in range(2, 8):

        iteration_scaling_op = run_lp_optimization(traffic_systems, iterations=i)
        #iteration_scaling_de = run_lp_decision(traffic_systems, iterations=i)

        save_results_as_json_files(iteration_scaling_op, str(i) + EXPERIMENT_FOLDER + "optimization/")
        #save_results_as_json_files(iteration_scaling_de, str(i) + EXPERIMENT_FOLDER + "decision/")

def main():
    run()

if __name__ == "__main__":
    main()