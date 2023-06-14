# Optimizing-Link-Utilization-During-Network-Migration
This is the reproducibility package for the 2023 computer science master thesis project *Optimizing Link Utilization During Network Migration* by Benjamin Nørlund Nielsen and Magnus Holm Lundbergh. 

## Platform
The package has been tested on Windows 10 (64-bit) and Ubuntu 22.04.2 LTS.

## Requirements
You will need Python 3.8 or newer.

## Windows installation
Before you begin, make sure pip is up-to-date by typing 'python -m pip install --upgrade pip' in a terminal.

First, you need to set up a virtual enviroment and install the required packages. Open a terminal in the project folder and type 'python -m venv venv'. After it is done, type 'venv\Scripts\activate' to activate the virtual environment. If everything went well, your terminal should now say something like '(env) C:\projects\Optimizing-Link-Utilization-During-Network-Migration'. Finally, type 'python -m pip install -r requirements.txt'. If it installs the packages listed in the requirements.txt file in the virtual environment, you should be good to go.

## Linux installation
Before you begin, make sure pip is up-to-date by typing 'python3 -m pip install --user --upgrade pip' in a terminal.

First, you need to set up a virtual enviroment and install the required packages. Open a terminal in the project folder and type 'python3 -m venv venv'. After it is done, type 'source venv/bin/activate' to activate the virtual environment. Finally, type 'python -m pip install -r requirements.txt'. If it installs the packages listed in the requirements.txt file in the virtual environment, you should be good to go.

## Running the package
If you haven't already, activate the virtual environment now. Make sure that the terminal is in the top-level of the project folder. Each experiment from the paper can be found in the 'experiment_setup' folder. To run an experiment, just run the corresponding python file by typing something like 'python experiment_setup/flow_removal_experiment.py'. The results can be found in the 'results' folder.

## Experiments overview
  -The length bound experiment from section 6.2 is called 'length_bound_experiment.py'. <br />
  -The decision LP experiment from section 6.3 is called 'decision_lp_experiment.py'. <br />
  -The monotonicity experiment from section 6.4 is called 'monotonicity_experiment.py'. <br />
  -The pruning experiment from section 6.5 is partitioned into 3 files called <br />
    -'pruning_experiment_flows.py', <br />
    -'pruning_experiment_edges.py', and <br />
    -'pruning_experiment_combined.py'. <br />
  -The flow removal experiment from section 6.6 is called 'flow_removal_experiment.py'. <br />
  -The combination of pruning and flow removal experiment from section 6.7 is called 'combination_of_pruning_and_flow_removal_experiment.py'.








