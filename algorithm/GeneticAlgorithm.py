import preprocessor.Preprocessor as Preprocessor
import random
import networkx as nx
from dataclasses import dataclass
import parser.Parser as Parser

#Constants
ALPHA = 15.0
BETA = 70.0
GENERATIONS = 50
POPULATION_SIZE = 50
STEPS = 6
MUTATION_RANDOM = 1
MUTATION_CROSSOVER = 15

@dataclass
class SingleUpdate:
    update_value: float
    flow: list
    affected_edges: list #list of 2-tuples displaying edges

@dataclass
class UpdateStep:
    update_step: list[SingleUpdate]

@dataclass
class UpdateSequence:
    update_matrix: list[UpdateStep]


def test_population_1():
    test_population = [[0, 0, 0], [0.2, 0.2, 0.2], [0.4, 0.4, 0.4], [0.6, 0.6, 0.6], [0.8, 0.8, 0.8], [1, 1, 1]]
    return test_population

def test_population_2():
    test_population = initialize_population()
    return test_population

def parse_problem():
    traffic_system = Parser.generate_traffic_systems(Parser.parse_flows(), Parser.parse_zoo_topologies_with_strict_capacity())

    parsed_problem = UpdateSequence

    for i in range(STEPS):
        parsed_problem.update_matrix.append()

    return traffic_system

def initialize_generation():
    first_generation = []
    for i in range(POPULATION_SIZE):
        first_generation.append(initialize_population())
    return first_generation

def generate_next_generation(ranked_generation):
    next_generation = []

    for population in ranked_generation[0]:
        next_generation.append(population)

    for population in ranked_generation[1]:
        new_population = standard_mutation(random.choice(ranked_generation[0]), population, MUTATION_CROSSOVER, MUTATION_RANDOM)
        next_generation.append(new_population)

    for population in ranked_generation[2]:
        new_population = initialize_population()
        next_generation.append(new_population)

    return next_generation

def initialize_population(): #consider different weightings such that it doesn't as quickly land at 0.999999
    initial_population = [[0, 0, 0]]
    previous_step = initial_population[0]
    for i in range(STEPS-1):
        if i+1 == STEPS-1:
            initial_population.append(final_step(previous_step))
        else:
            previous_step = random_increasing_population_step(previous_step)
            initial_population.append(previous_step)

    return initial_population

def random_increasing_population_step(previous_step):
    step = []
    for item in previous_step:
        step.append(random.uniform(item, 1))
    return step

def random_population_step(previous_step):
    step = []
    for item in previous_step:
        step.append(random.uniform(0, 1))
    return step

def final_step(previous_step):
    step = []
    for amount_of_steps in previous_step:
        step.append(1)
    return step

def evaluate_population(population): #change to return both the population with evaluation
    worst_evaluation = 0.0
    for steps in population:
        evaluation = evaluate(steps)

        if evaluation > worst_evaluation:
            worst_evaluation = evaluation

    return worst_evaluation

def evaluate(graph, step): #wip
    for edge in graph.edges:

        edge['capacity']
    return 0

def rank_populations(generation): #reconsider naming scheme
    ranked_populations = [[], [], []]
    for populations in generation:
        ranked_populations.append(evaluate_population(populations))

    return ranked_populations

def mutate_generation(generation):
    return

def mutate_population(population_evaluation): # different ways of going about
    return

def approximation_mutation(elite_population, common_population, mutation_rate): #don't work on this too much currently

    for steps in common_population:
        mutation_chance = random.randint(0, 100)
        if mutation_chance > mutation_rate:
            i = 0

def standard_mutation(elite_population, common_population, mutation_rate_crossover, mutation_rate_random):
    new_population = common_population
    for steps in range(len(new_population)):
        for update in range(len(new_population[0])):
            rng = random.randrange(1, 101)
            if rng <= mutation_rate_random:
                new_population[steps][update] = random.uniform(0, 1)
                print("mutate random")
            elif rng <= mutation_rate_crossover + mutation_rate_random:
                new_population[steps][update] = elite_population[steps][update]
                print("mutate crossover")
            else:
                print("no mutation")

    return new_population

def run_genetic_algorithm(traffic_problem): #consider adding different things such that nice meta information is returned as well
    all_generations = []

    initial_generation = initialize_generation()
    all_generations.append(initial_generation)
    current_generation = initial_generation

    for i in range(GENERATIONS):
        ranked_generation = rank_populations(current_generation)
        current_generation = generate_next_generation(ranked_generation)
        all_generations.append(current_generation)

    return

def main():
    print("Hello World!")
    #print(standard_mutation(test_population_1(), test_population_2(), 15, 1))
    P = Parser.generate_traffic_systems(Parser.parse_flows(), Parser.parse_zoo_topologies_with_strict_capacity())
    G = P[0].topology
    print(P[0].topology)
    print(P[0])
    for node1, node2, data in G.edges(data=True):
        print(data['capacity'])

if __name__ == "__main__":
    main()