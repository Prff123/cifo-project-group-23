from random import choice, random
from copy import deepcopy
from operator import attrgetter
import time


class Individual:
    def __init__(self, representation=None, size=None, generated_map=None, fruit_points=1000, points=100,
                 history_state=False, stepback=False):

        valid_set = ("L", "D", "R", "U")

        if representation is None:
            self.representation = [choice(valid_set) for _ in range(size)]
        else:
            self.representation = representation

        self.map = deepcopy(generated_map)
        self.position = [0, 0]

        #point system
        self.fruit_points = fruit_points
        self.points = points

        if stepback:
            self.stepback = self.points / 2
        else:
            self.stepback = 0

        self.history_state = history_state
        if self.history_state:
            self.history = []

        self.fitness = self.get_fitness()

    def get_fitness(self):
        # Parameters
        pacman_pos = self.position
        finish_flag = False
        fitness = 0

        fruits_left = 0
        points_left = 0

        for row in self.map:
            for item in row:
                if item == "*":
                    points_left += 1

                elif item == "f":
                    fruits_left += 1

        while finish_flag is False:
            for move in self.representation:

                if self.history_state:
                    self.history.append((deepcopy(self.map), fitness))

                # move left
                if move == "L":

                    # in case it is in the left most position of that row
                    if pacman_pos[1] == 0:

                        # in case it is in the left most position of that row and the right most position has a ghost
                        if self.map[pacman_pos[0]][len(self.map[0]) - 1] == "g":

                            self.map[pacman_pos[0]][pacman_pos[1]] = "_"  # the spot where pacman was is now empty
                            pacman_pos = [pacman_pos[0], len(self.map[0]) - 1]  # we change the position of pacman
                            self.map[pacman_pos[0]][pacman_pos[1]] = "p"  # this spot in map is now where pacman is

                            finish_flag = True  # it finishes the game by touching a ghost
                            break

                        # in case it is in the left most position of that row and the right most position is a point
                        elif self.map[pacman_pos[0]][len(self.map[0]) - 1] == "*":

                            fitness += self.points  # increases fitness for collecting a point
                            self.map[pacman_pos[0]][pacman_pos[1]] = "_"  # the spot where pacman was is now empty
                            pacman_pos = [pacman_pos[0], len(self.map[0]) - 1]  # we change the position of pacman
                            self.map[pacman_pos[0]][pacman_pos[1]] = "p"  # this spot in map is now where pacman is
                            points_left -= 1

                            if points_left == 0 and fruits_left == 0:
                                finish_flag = True
                                break
                            continue

                        # in case it is in the left most position of that row and the right most position is a fruit
                        elif self.map[pacman_pos[0]][len(self.map[0]) - 1] == "f":

                            fitness += self.fruit_points  # increases fitness for collecting a fruit
                            self.map[pacman_pos[0]][pacman_pos[1]] = "_"  # the spot where pacman was is now empty
                            pacman_pos = [pacman_pos[0], len(self.map[0]) - 1]  # we change the position of pacman
                            self.map[pacman_pos[0]][pacman_pos[1]] = "p"  # this spot in map is now where pacman is

                            fruits_left -= 1
                            if points_left == 0 and fruits_left == 0:
                                finish_flag = True
                                break
                            continue

                        # in case it is in the left most position of that row and the right most position is an empty space
                        elif self.map[pacman_pos[0]][len(self.map[0]) - 1] == "_":

                            fitness -= self.stepback # decreases fitness for stepping an empty spot
                            self.map[pacman_pos[0]][pacman_pos[1]] = "_"  # the spot where pacman was is now empty
                            pacman_pos = [pacman_pos[0], len(self.map[0]) - 1]  # we change the position of pacman
                            self.map[pacman_pos[0]][pacman_pos[1]] = "p"  # this spot in map is now where pacman is

                            continue

                    # if the left spot has a ghost
                    elif self.map[pacman_pos[0]][pacman_pos[1] - 1] == "g":

                        self.map[pacman_pos[0]][pacman_pos[1]] = "_"  # the spot where pacman was is now empty
                        pacman_pos = [pacman_pos[0], pacman_pos[1] - 1]  # we change the position of pacman
                        self.map[pacman_pos[0]][pacman_pos[1]] = "p"  # this spot in map is now where pacman is

                        finish_flag = True  # it finishes the game by touching a ghost
                        break

                    # if the left spot has a point
                    elif self.map[pacman_pos[0]][pacman_pos[1] - 1] == "*":

                        fitness += self.points  # increases fitness for collecting a point
                        self.map[pacman_pos[0]][pacman_pos[1]] = "_"  # the spot where pacman was is now empty
                        pacman_pos = [pacman_pos[0], pacman_pos[1] - 1]  # we change the position of pacman
                        self.map[pacman_pos[0]][pacman_pos[1]] = "p"  # this spot in map is now where pacman is

                        points_left -= 1
                        if points_left == 0 and fruits_left == 0:
                            finish_flag = True
                            break
                        continue

                    # if the left spot has a fruit
                    elif self.map[pacman_pos[0]][pacman_pos[1] - 1] == "f":

                        fitness += self.fruit_points  # increases fitness for collecting a point
                        self.map[pacman_pos[0]][pacman_pos[1]] = "_"  # the spot where pacman was is now empty
                        pacman_pos = [pacman_pos[0], pacman_pos[1] - 1]  # we change the position of pacman
                        self.map[pacman_pos[0]][pacman_pos[1]] = "p"  # this spot in map is now where pacman is

                        fruits_left -= 1
                        if points_left == 0 and fruits_left == 0:
                            finish_flag = True
                            break
                        continue

                    # if the left spot is empty
                    elif self.map[pacman_pos[0]][pacman_pos[1] - 1] == "_":

                        fitness -= self.stepback # decreases fitness for stepping an empty spot
                        self.map[pacman_pos[0]][pacman_pos[1]] = "_"  # the spot where pacman was is now empty
                        pacman_pos = [pacman_pos[0], pacman_pos[1] - 1]  # we change the position of pacman
                        self.map[pacman_pos[0]][pacman_pos[1]] = "p"  # this spot in map is now where pacman is

                        continue

                # move down
                if move == "D":

                    # in case pacman is in the down most position
                    if pacman_pos[0] == (len(self.map) - 1):

                        # in case pacman is in the down most position of that column and the up most position has a ghost
                        if self.map[0][pacman_pos[1]] == "g":

                            self.map[pacman_pos[0]][pacman_pos[1]] = "_"  # the spot where pacman was is now empty
                            pacman_pos = [0, pacman_pos[1]]  # we change the position of pacman
                            self.map[pacman_pos[0]][pacman_pos[1]] = "p"  # this spot in map is now where pacman is

                            finish_flag = True  # it finishes the game by touching a ghost
                            break

                        # in case pacman is in the down most position of that column and the up most position has a point
                        elif self.map[0][pacman_pos[1]] == "*":

                            fitness += self.points  # increases fitness for collecting a point
                            self.map[pacman_pos[0]][pacman_pos[1]] = "_"  # the spot where pacman was is now empty
                            pacman_pos = [0, pacman_pos[1]]  # we change the position of pacman
                            self.map[pacman_pos[0]][pacman_pos[1]] = "p"  # this spot in map is now where pacman is

                            points_left -= 1
                            if points_left == 0 and fruits_left == 0:
                                finish_flag = True
                                break
                            continue

                        # in case pacman is in the down most position of that column and the up most position has a fruit
                        elif self.map[0][pacman_pos[1]] == "f":

                            fitness += self.fruit_points  # increases fitness for collecting a fruit
                            self.map[pacman_pos[0]][pacman_pos[1]] = "_"  # the spot where pacman was is now empty
                            pacman_pos = [0, pacman_pos[1]]  # we change the position of pacman
                            self.map[pacman_pos[0]][pacman_pos[1]] = "p"  # this spot in map is now where pacman is

                            fruits_left -= 1
                            if points_left == 0 and fruits_left == 0:
                                finish_flag = True
                                break
                            continue

                        # in case pacman is in the down most position of that column and the up most position is empty
                        elif self.map[0][pacman_pos[1]] == "_":

                            fitness -= self.stepback # decreases fitness for stepping an empty spot
                            self.map[pacman_pos[0]][pacman_pos[1]] = "_"  # the spot where pacman was is now empty
                            pacman_pos = [0, pacman_pos[1]]  # we change the position of pacman
                            self.map[pacman_pos[0]][pacman_pos[1]] = "p"  # this spot in map is now where pacman is

                            continue

                    # if the down position has a ghost
                    elif self.map[pacman_pos[0] + 1][pacman_pos[1]] == "g":

                        self.map[pacman_pos[0]][pacman_pos[1]] = "_"  # the spot where pacman was is now empty
                        pacman_pos = [pacman_pos[0] + 1, pacman_pos[1]]  # we change the position of pacman
                        self.map[pacman_pos[0]][pacman_pos[1]] = "p"  # this spot in map is now where pacman is

                        finish_flag = True  # it finishes the game by touching a ghost
                        break

                    # if the down spot has a point
                    elif self.map[pacman_pos[0] + 1][pacman_pos[1]] == "*":

                        fitness += self.points  # increases fitness for collecting a point
                        self.map[pacman_pos[0]][pacman_pos[1]] = "_"  # the spot where pacman was is now empty
                        pacman_pos = [pacman_pos[0] + 1, pacman_pos[1]]  # we change the position of pacman
                        self.map[pacman_pos[0]][pacman_pos[1]] = "p"  # this spot in map is now where pacman is

                        points_left -= 1
                        if points_left == 0 and fruits_left == 0:
                            finish_flag = True
                            break
                        continue

                    # if the down spot has a fruit
                    elif self.map[pacman_pos[0] + 1][pacman_pos[1]] == "f":

                        fitness += self.fruit_points  # increases fitness for collecting a fruit
                        self.map[pacman_pos[0]][pacman_pos[1]] = "_"  # the spot where pacman was is now empty
                        pacman_pos = [pacman_pos[0] + 1, pacman_pos[1]]  # we change the position of pacman
                        self.map[pacman_pos[0]][pacman_pos[1]] = "p"  # this spot in map is now where pacman is

                        fruits_left -= 1
                        if points_left == 0 and fruits_left == 0:
                            finish_flag = True
                            break
                        continue

                    # if the down spot is empty
                    elif self.map[pacman_pos[0] + 1][pacman_pos[1]] == "_":

                        fitness -= self.stepback # decreases fitness for stepping an empty spot
                        self.map[pacman_pos[0]][pacman_pos[1]] = "_"  # the spot where pacman was is now empty
                        pacman_pos = [pacman_pos[0] + 1, pacman_pos[1]]  # we change the position of pacman
                        self.map[pacman_pos[0]][pacman_pos[1]] = "p"  # this spot in map is now where pacman is

                        continue

                # move right
                elif move == "R":

                    # in case it is in the right most position
                    if pacman_pos[1] == (len(self.map[0]) - 1):

                        # in case it is in the right most position of that row and the left most position has a ghost
                        if self.map[pacman_pos[0]][0] == "g":

                            self.map[pacman_pos[0]][pacman_pos[1]] = "_"  # the spot where pacman was is now empty
                            pacman_pos = [pacman_pos[0], 0]  # we change the position of pacman
                            self.map[pacman_pos[0]][pacman_pos[1]] = "p"  # this spot in map is now where pacman is

                            finish_flag = True  # it finishes the game by touching a ghost
                            break

                        # in case it is in the right most position of that row and the left most position is a point
                        elif self.map[pacman_pos[0]][0] == "*":

                            fitness += self.points  # increases fitness for collecting a point
                            self.map[pacman_pos[0]][pacman_pos[1]] = "_"  # the spot where pacman was is now empty
                            pacman_pos = [pacman_pos[0], 0]  # we change the position of pacman
                            self.map[pacman_pos[0]][pacman_pos[1]] = "p"  # this spot in map is now where pacman is

                            points_left -= 1
                            if points_left == 0 and fruits_left == 0:
                                finish_flag = True
                                break
                            continue

                        # in case it is in the right most position of that row and the left most position is a fruit
                        elif self.map[pacman_pos[0]][0] == "f":

                            fitness += self.points  # increases fitness for collecting a fruit
                            self.map[pacman_pos[0]][pacman_pos[1]] = "_"  # the spot where pacman was is now empty
                            pacman_pos = [pacman_pos[0], 0]  # we change the position of pacman
                            self.map[pacman_pos[0]][pacman_pos[1]] = "p"  # this spot in map is now where pacman is

                            fruits_left -= 1
                            if points_left == 0 and fruits_left == 0:
                                finish_flag = True
                                break
                            continue

                        # in case it is in the right most position of that row and the left most position is an empty space
                        elif self.map[pacman_pos[0]][0] == "_":

                            fitness -= self.stepback # decreases fitness for stepping an empty spot
                            self.map[pacman_pos[0]][pacman_pos[1]] = "_"  # the spot where pacman was is now empty
                            pacman_pos = [pacman_pos[0], 0]  # we change the position of pacman
                            self.map[pacman_pos[0]][pacman_pos[1]] = "p"  # this spot in map is now where pacman is

                            continue

                    # if the right spot has a ghost
                    elif self.map[pacman_pos[0]][pacman_pos[1] + 1] == "g":

                        self.map[pacman_pos[0]][pacman_pos[1]] = "_"  # the spot where pacman was is now empty
                        pacman_pos = [pacman_pos[0], pacman_pos[1] + 1]  # we change the position of pacman
                        self.map[pacman_pos[0]][pacman_pos[1]] = "p"  # this spot in map is now where pacman is

                        finish_flag = True  # it finishes the game by touching a ghost
                        break

                    # if the right spot has a point
                    elif self.map[pacman_pos[0]][pacman_pos[1] + 1] == "*":

                        fitness += self.points  # increases fitness for collecting a point
                        self.map[pacman_pos[0]][pacman_pos[1]] = "_"  # the spot where pacman was is now empty
                        pacman_pos = [pacman_pos[0], pacman_pos[1] + 1]  # we change the position of pacman
                        self.map[pacman_pos[0]][pacman_pos[1]] = "p"  # this spot in map is now where pacman is

                        points_left -= 1
                        if points_left == 0 and fruits_left == 0:
                            finish_flag = True
                            break
                        continue

                    # if the right spot has a fruit
                    elif self.map[pacman_pos[0]][pacman_pos[1] + 1] == "f":

                        fitness += self.fruit_points  # increases fitness for collecting a fruit
                        self.map[pacman_pos[0]][pacman_pos[1]] = "_"  # the spot where pacman was is now empty
                        pacman_pos = [pacman_pos[0], pacman_pos[1] + 1]  # we change the position of pacman
                        self.map[pacman_pos[0]][pacman_pos[1]] = "p"  # this spot in map is now where pacman is

                        fruits_left -= 1
                        if points_left == 0 and fruits_left == 0:
                            finish_flag = True
                            break
                        continue

                    # if the right spot is empty
                    elif self.map[pacman_pos[0]][pacman_pos[1] + 1] == "_":

                        fitness -= self.stepback # decreases fitness for stepping an empty spot
                        self.map[pacman_pos[0]][pacman_pos[1]] = "_"  # the spot where pacman was is now empty
                        pacman_pos = [pacman_pos[0], pacman_pos[1] + 1]  # we change the position of pacman
                        self.map[pacman_pos[0]][pacman_pos[1]] = "p"  # this spot in map is now where pacman is

                        continue

                # move up
                elif move == "U":

                    if pacman_pos[0] == 0:

                        # in case pacman is in the up most position of that column and the up down position has a ghost
                        if self.map[len(self.map) - 1][pacman_pos[1]] == "g":

                            self.map[pacman_pos[0]][pacman_pos[1]] = "_"  # the spot where pacman was is now empty
                            pacman_pos = [len(self.map) - 1, pacman_pos[1]]  # we change the position of pacman
                            self.map[pacman_pos[0]][pacman_pos[1]] = "p"  # this spot in map is now where pacman is

                            finish_flag = True  # it finishes the game by touching a ghost
                            break

                        # in case pacman is in the up most position of that column and the down most position has a point
                        elif self.map[len(self.map) - 1][pacman_pos[1]] == "*":

                            fitness += self.points  # increases fitness for collecting a point
                            self.map[pacman_pos[0]][pacman_pos[1]] = "_"  # the spot where pacman was is now empty
                            pacman_pos = [len(self.map) - 1, pacman_pos[1]]  # we change the position of pacman
                            self.map[pacman_pos[0]][pacman_pos[1]] = "p"  # this spot in map is now where pacman is

                            points_left -= 1
                            if points_left == 0 and fruits_left == 0:
                                finish_flag = True
                                break
                            continue

                        # in case pacman is in the up most position of that column and the down most position has a fruit
                        elif self.map[len(self.map) - 1][pacman_pos[1]] == "f":

                            fitness += self.points  # increases fitness for collecting a point
                            self.map[pacman_pos[0]][pacman_pos[1]] = "_"  # the spot where pacman was is now empty
                            pacman_pos = [len(self.map) - 1, pacman_pos[1]]  # we change the position of pacman
                            self.map[pacman_pos[0]][pacman_pos[1]] = "p"  # this spot in map is now where pacman is

                            fruits_left -= 1
                            if points_left == 0 and fruits_left == 0:
                                finish_flag = True
                                break
                            continue

                        # in case pacman is in the up most position of that column and the down most position is empty
                        elif self.map[len(self.map) - 1][pacman_pos[1]] == "_":

                            fitness -= self.stepback # decreases fitness for stepping an empty spot
                            self.map[pacman_pos[0]][pacman_pos[1]] = "_"  # the spot where pacman was is now empty
                            pacman_pos = [len(self.map) - 1, pacman_pos[1]]  # we change the position of pacman
                            self.map[pacman_pos[0]][pacman_pos[1]] = "p"  # this spot in map is now where pacman is

                            continue

                    # if the up position has a ghost
                    elif self.map[pacman_pos[0] - 1][pacman_pos[1]] == "g":

                        self.map[pacman_pos[0]][pacman_pos[1]] = "_"  # the spot where pacman was is now empty
                        pacman_pos = [pacman_pos[0] - 1, pacman_pos[1]]  # we change the position of pacman
                        self.map[pacman_pos[0]][pacman_pos[1]] = "p"  # this spot in map is now where pacman is

                        finish_flag = True  # it finishes the game by touching a ghost
                        break

                    # if the up spot has a point
                    elif self.map[pacman_pos[0] - 1][pacman_pos[1]] == "*":

                        fitness += self.points  # increases fitness for collecting a point
                        self.map[pacman_pos[0]][pacman_pos[1]] = "_"  # the spot where pacman was is now empty
                        pacman_pos = [pacman_pos[0] - 1, pacman_pos[1]]  # we change the position of pacman
                        self.map[pacman_pos[0]][pacman_pos[1]] = "p"  # this spot in map is now where pacman is

                        points_left -= 1
                        if points_left == 0 and fruits_left == 0:
                            finish_flag = True
                            break
                        continue

                    # if the down spot has a fruit
                    elif self.map[pacman_pos[0] - 1][pacman_pos[1]] == "f":

                        fitness += self.fruit_points  # increases fitness for collecting a fruit
                        self.map[pacman_pos[0]][pacman_pos[1]] = "_"  # the spot where pacman was is now empty
                        pacman_pos = [pacman_pos[0] - 1, pacman_pos[1]]  # we change the position of pacman
                        self.map[pacman_pos[0]][pacman_pos[1]] = "p"  # this spot in map is now where pacman is

                        fruits_left -= 1
                        if points_left == 0 and fruits_left == 0:
                            finish_flag = True
                            break
                        continue

                    # if the down spot is empty
                    elif self.map[pacman_pos[0] - 1][pacman_pos[1]] == "_":

                        fitness -= self.stepback # decreases fitness for stepping an empty spot
                        self.map[pacman_pos[0]][pacman_pos[1]] = "_"  # the spot where pacman was is now empty
                        pacman_pos = [pacman_pos[0] - 1, pacman_pos[1]]  # we change the position of pacman
                        self.map[pacman_pos[0]][pacman_pos[1]] = "p"  # this spot in map is now where pacman is

                        continue

            finish_flag = True

        if self.history_state:
            self.history.append((deepcopy(self.map), fitness)) # append final map_state

        return fitness

    def get_history(self):

        if self.history_state is True:  # prints every map_state with 0.5 seconds of delay
            for step in self.history:
                for row in step[0]:
                    print(row)
                print("Current Fitness:", step[1])
                time.sleep(0.5)
                print("\n")

        else:  #in case the history_state wasn't turned on and the user asks for it to be printed
            print("Error: history_state is set to False, no history is stored")

    def index(self, value):
        return self.representation.index(value)

    def __len__(self):
        return len(self.representation)

    def __getitem__(self, position):
        return self.representation[position]

    def __setitem__(self, position, value):
        self.representation[position] = value

    def __repr__(self):
        return f"Individual(Fitness: {self.fitness};Moves={self.representation})"


class Population:
    def __init__(self, size, generated_map, moves=20, fruit_points=1000, points=100, stepback=False):
        self.individuals = []
        self.size = size
        self.original_map = deepcopy(generated_map)
        self.map = deepcopy(generated_map)
        self.moves = moves
        self.fruit_points = fruit_points
        self.points = points
        self.best_individuals_gen = []
        self.stepback = stepback

        for i in range(size):
            self.individuals.append(
                Individual(size=self.moves,
                           generated_map=self.map,
                           fruit_points=self.fruit_points,
                           points=self.points,
                           stepback=self.stepback
                           )
            )

        self.best_individual = max(self.individuals, key=attrgetter("fitness"))

    def evolve(self, gens, xo_prob, mut_prob, select, mutate, crossover, elitism=True):

        for i in range(gens):
            new_pop = []

            # if elitism is True, stores the population best_individual in elite variable
            if elitism:
                elite = self.best_individual

            while len(new_pop) < self.size:

                # selection
                parent1, parent2 = select(self), select(self)

                # crossover
                if random() < xo_prob:
                    offspring1, offspring2 = crossover(parent1, parent2)
                else:
                    offspring1 = parent1.representation
                    offspring2 = parent2.representation

                # mutation
                if random() < mut_prob:
                    offspring1 = mutate(offspring1)
                if random() < mut_prob:
                    offspring2 = mutate(offspring2)

                new_pop.append(Individual(representation=offspring1, generated_map=self.original_map,
                                          fruit_points=self.fruit_points, points=self.points, stepback=self.stepback))
                if len(new_pop) < self.size:
                    new_pop.append(Individual(representation=offspring2, generated_map=self.original_map,
                                              fruit_points=self.fruit_points, points=self.points,
                                              stepback=self.stepback))

            # if elitism is True, the worst Individual from the new population,
            # if worse than the previous generation best individual, is swaped by the previous best_individual
            if elitism:
                worst = min(new_pop, key=attrgetter("fitness"))
                if elite.fitness > worst.fitness:
                    new_pop.pop(new_pop.index(worst))
                    new_pop.append(elite)

            self.individuals = new_pop

            # store the best individual from each generation
            self.best_individuals_gen.append(max(self.individuals, key=attrgetter("fitness")))

            # update the population best overall individual if there is a new best
            if max(self.individuals, key=attrgetter("fitness")).fitness > self.best_individual.fitness:
                self.best_individual = Individual(representation=max(self.individuals, key=attrgetter("fitness")).representation,
                                              generated_map=self.original_map, fruit_points=self.fruit_points,
                                              points=self.points, history_state=False, stepback=self.stepback)



            # prints the best individual for that generation, like a verbose.
            print(f'Gen {i+1} Best Individual: {max(self.individuals, key=attrgetter("fitness"))}')

        # The final best individual is "recreated" to allow for its game to be stored so that it can be played later with the "get_history" function
        self.best_individual = Individual(representation=self.best_individual.representation,
                                          generated_map=self.original_map, fruit_points=self.fruit_points,
                                          points=self.points, history_state=True, stepback=self.stepback)

    def __len__(self):
        return len(self.individuals)

    def __getitem__(self, position):
        return self.individuals[position]
