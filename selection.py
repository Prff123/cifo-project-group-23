from random import uniform, choice, choices
import math
from operator import attrgetter


def fps(population):
    """Fitness proportionate selection implementation.

    Args:
        population (Population): The population we want to select from.

    Returns:
        Individual: selected individual.
    """
    # Sum total fitness
    total_fitness = sum([i.fitness for i in population])
    # Get a 'position' on the wheel
    spin = uniform(0, total_fitness)
    position = 0
    # Find individual in the position of the spin
    for individual in population.individuals:
        position += individual.fitness
        if position > spin:
            return individual


def tournament_sel(population, size=5):
    """Tournament selection implementation.

    Description: Select individuals based on tournament size with replacement.

    Args:
        population (Population): The population we want to select from.
        size (int): Size of the tournament.

    Returns:
        Individual: The best individual in the tournament.
    """

    tournament = [choice(population.individuals) for _ in range(size)]

    return max(tournament, key=attrgetter("fitness"))


def boltzmann_selection(population, temperature=0.5):
    """Implementation of rank-based selection.

    Description: Assigns higher probabilities to individuals with higher fitness values,
                 with the degree of preference controlled by the temperature parameter.
                 Higher temperatures result in a more uniform distribution of probabilities,
                 while lower temperatures lead to more selective pressure favoring individuals
                 with higher fitness values.

    Args:
        population (list): List of individuals in the population.

    Returns:
        list: List of selected parents.
    """

    fitness_values = [individual.fitness for individual in population]
    max_fitness = max(fitness_values)

    scaled_fitness_values = [fitness_value - max_fitness for fitness_value in fitness_values]

    sum_exp = sum(math.exp(fitness_value/temperature) for fitness_value in scaled_fitness_values)
    probabilities = [math.exp(fitness_value/temperature)/sum_exp for fitness_value in scaled_fitness_values]

    selected_individual = choices(population, probabilities)[0]
    return selected_individual


def rank_based_selection(population):
    """Implementation of rank-based selection.

    Description: Assigns higher probabilities to individuals with better fitness ranks, 
                 which encourages the selection of fitter individuals while maintaining 
                 some diversity in the population.

    Args:
        population (list): List of individuals in the population.

    Returns:
        list: List of selected parents.
    """
    population_size = len(population)
    ranks = sorted(range(population_size), key=lambda x: population[x].fitness)
    selection_probabilities = [(2*(population_size - i))/(population_size*(population_size + 1)) for i in ranks]

    selected_parent = choices(population, weights=selection_probabilities, k=1)[0]

    return selected_parent
