import parser.Parser as Parser

lpo_file_directory = "latex_plots/logLPO.txt"
#lpd_file_directory = "latex_plots/logLPD.txt"
#mipo_file_directory = "latex_plots/logMIPO.txt"
#mipd_file_directory = "latex_plots/logMIPD.txt"

def get_logs_as_cactus_plot():
    list_of_logs = Parser.parse_logs()
    list_of_logs = sorted(list_of_logs, key=lambda x: x['solve_time'])

    print_file = "\\addplot[mark=none, color=orange, solid, thick] coordinates{"

    log_iterator = 0

    for logs in list_of_logs:
        print_file += ("(" + str(log_iterator) + ", " + str(logs['solve_time']) + ")")
        log_iterator += 1

    print_file +="};"

    return print_file

def write_test_data_as_file(data, directory):
    data_file = open(directory, "w")
    data_file.write(data)
    data_file.close()
    return

def save_logs_solution_time_over_amount_of_nodes():
    list_of_logs = Parser.parse_logs()
    list_of_topologies = Parser.parse_zoo_topologies()

    return

def main():
    write_test_data_as_file(get_logs_as_cactus_plot(), lpo_file_directory)


if __name__ == "__main__":
    main()