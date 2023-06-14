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

EXPERIMENT_FOLDER = 'monotonic_experiment/'

def run():
    traffic_systems = Preprocessor.produce_traffic_systems()


    monotonic_problem_op = run_lp_optimization(traffic_systems, monotonic=True)
    #monotonic_problem_de = run_lp_decision(traffic_systems, monotonic=True)

    save_results_as_json_files(monotonic_problem_op, EXPERIMENT_FOLDER + "optimization/")
    #save_results_as_json_files(monotonic_problem_de, EXPERIMENT_FOLDER + "decision/")

def main():
    run()

if __name__ == "__main__":
    main()