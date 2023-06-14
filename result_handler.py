import sys
sys.path.append('./')
from constants import RESULT_PATH
import os
import json

def save_results_as_json_files(results, path_name): #Results are expected to be a list of dicts of results from algorithms
    folder = RESULT_PATH + path_name
    os.makedirs(folder, exist_ok=True)
    for result in results:
        f = open(folder + result['label'] + '.json', "w")
        json.dump(result, f)
        f.close()