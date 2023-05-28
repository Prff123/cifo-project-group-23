from random import randint, sample, choice


def move_mutation(individual):
    """Move mutation for a GA individual

    Description: Changes one random move in the representation for a different one included in the valid set.

    Args:
        individual (Individual): A GA individual from charles.py

    Returns:
        Individual: Mutated Individual
    """

    mut_index = randint(0, len(individual) - 1)

    if individual[mut_index] == "L":
        individual[mut_index] = choice(("D", "R", "U"))
    elif individual[mut_index] == "D":
        individual[mut_index] = choice(("L", "R", "U"))
    elif individual[mut_index] == "R":
        individual[mut_index] = choice(("L", "D", "U"))
    elif individual[mut_index] == "U":
        individual[mut_index] = choice(("L", "R", "D"))

    return individual


def swap_mutation(individual):
    """Swap mutation for a GA individual.

    Description: Swaps two random items in the Individual's representation.

    Args:
        individual (Individual): A GA individual from charles.py

    Returns:
        Individual: Mutated Individual
    """

    mut_indexes = sample(range(0, len(individual)), 2)
    individual[mut_indexes[0]], individual[mut_indexes[1]] = individual[mut_indexes[1]], individual[mut_indexes[0]]
    return individual


def inversion_mutation(individual):
    """Inversion mutation for a GA individual.

    Description: Reverts a portion of the representation.

    Args:
        individual (Individual): A GA individual from charles.py

    Returns:
        Individual: Mutated Individual
    """
    mut_indexes = sample(range(0, len(individual)), 2)
    #mut_indexes = [0,3]
    mut_indexes.sort()
    individual[mut_indexes[0]:mut_indexes[1]] = individual[mut_indexes[0]:mut_indexes[1]][::-1]
    return individual


