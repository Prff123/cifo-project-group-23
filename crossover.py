from random import randint, sample, random


def single_point_co(p1, p2):
    """Implementation of single point crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    co_point = randint(1, len(p1)-2)

    offspring1 = p1[:co_point] + p2[co_point:]
    offspring2 = p2[:co_point] + p1[co_point:]

    return offspring1, offspring2


def multi_point_co(p1, p2, num_points=5):
    """Implementation of multi-point crossover.

    Description: Similar to the single_point_co, but with more crossover points.
                 Alternating segments are swapped to get new offsprings.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.
        num_points (int): Number of crossover points.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    max_points = min(len(p1) - 1, len(p2) - 1, num_points)
    points = sorted(sample(range(1, len(p1)), max_points))

    offspring1 = p1[:]
    offspring2 = p2[:]

    for i in range(len(points)):
        if i % 2 == 0:
            offspring1[points[i-1]:points[i]] = p2[points[i-1]:points[i]]
            offspring2[points[i-1]:points[i]] = p1[points[i-1]:points[i]]
        else:
            offspring1[points[i-1]:points[i]] = p1[points[i-1]:points[i]]
            offspring2[points[i-1]:points[i]] = p2[points[i-1]:points[i]]

    return offspring1, offspring2


def uniform_co(p1, p2, probability=0.5):
    """Implementation of uniform crossover.

    Description: For each ith item in the parents' representation, it swaps them with some probability (0.5 default).

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.
        probability (float): Probability of swapping each gene.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    offspring1 = []
    offspring2 = []

    for i in range(len(p1)):
        if random() < probability:
            offspring1.append(p2[i])
            offspring2.append(p1[i])
        else:
            offspring1.append(p1[i])
            offspring2.append(p2[i])

    return offspring1, offspring2
