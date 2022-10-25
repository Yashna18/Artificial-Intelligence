__author__ = "Yashna Shetty"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "sheya140@student.otago.ac.nz"

import numpy as np
import random

agentName = "my_agent"
perceptFieldOfVision = 3  # Choose either 3,5,7 or 9
perceptFrames = 1  # Choose either 1,2,3 or 4
trainingSchedule = [("self", 150), ("random", 100)]
mutationChance = 0.05  # chance of mutation


# This is the class for your snake/agent
class Snake:

    def __init__(self, nPercepts, actions):
        # You should initialise self.chromosome member variable here (whatever you choose it
        # to be - a list/vector/matrix of numbers - and initialise it with some random
        # values)

        self.nPercepts = nPercepts
        self.actions = actions

        # Snake objects will have 3 chromosomes each
        # with them all correlating to a different action

        self.chromosome1 = np.random.uniform(-10, 10, (perceptFieldOfVision, perceptFieldOfVision + 1))
        self.chromosome2 = np.random.uniform(-10, 10, (perceptFieldOfVision, perceptFieldOfVision + 1))
        self.chromosome3 = np.random.uniform(-10, 10, (perceptFieldOfVision, perceptFieldOfVision + 1))

    # Agent function to map percepts to actions via chromosomes initialised in main function
    # Returns action to be performed

    def AgentFunction(self, percepts):
        # You should implement a model here that translates from 'percepts' to 'actions'
        # through 'self.chromosome'.
        #
        # The 'actions' variable must be returned, and it must be a 3-item list or 3-dim numpy vector

        #
        # The index of the largest numbers in the 'actions' vector/list is the action taken
        # with the following interpretation:
        # 0 - move left
        # 1 - move forward
        # 2 - move right
        #
        #
        # Different 'percepts' values should lead to different 'actions'.  This way the agent
        # reacts differently to different situations.
        #
        # Different 'self.chromosome' should lead to different 'actions'.  This way different
        # agents can exhibit different behaviour.

        # .
        # .
        # .

        # Chromosomes of the snakes are made of the chromosome,
        # and the bias of each chromosome in the last column

        w1 = self.chromosome1[:, :-1]
        b1 = self.chromosome1[:, -1:]
        w2 = self.chromosome2[:, :-1]
        b2 = self.chromosome2[:, -1:]
        w3 = self.chromosome3[:, :-1]
        b3 = self.chromosome3[:, -1:]

        # Agent function calculations as done by
        # multiplication of chromosome and input
        # and addition of bias

        v1 = np.matmul(percepts[-1], w1) + b1  # if largest, returns -1
        v2 = np.matmul(percepts[-1], w2) + b2  # if largest, returns 1
        v3 = np.matmul(percepts[-1], w3) + b3  # if largest, returns 0

        # find largest of the 3 summations
        # and return the index
        # index of largest result maps to the index of the action
        # that needs to be performed

        results = [np.linalg.det(v1), np.linalg.det(v3), np.linalg.det(v2)]
        index = np.argmax(results)

        # index = np.random.randint(low=0, high=len(self.actions))
        return self.actions[index]


# evaluates fitness of population passed via params

def evalFitness(population):
    N = len(population)

    # Fitness initialiser for all agents
    fitness = np.zeros((N))

    # This loop iterates over your agents in the old population - the purpose of this boiler plate
    # code is to demonstrate how to fetch information from the old_population in order
    # to score fitness of each agent
    for n, snake in enumerate(population):
        # snake is an instance of Snake class that you implemented above, therefore you can access any attributes
        # (such as `self.chromosome').  Additionally, the object has the following attributes provided by the
        # game engine:
        #
        # snake.size - list of snake sizes over the game turns
        # .
        # .
        # .
        maxSize = np.max(snake.sizes)
        turnsAlive = np.sum(snake.sizes > 0)
        maxTurns = len(snake.sizes)

        # This fitness functions considers snake size plus the fraction of turns the snake
        # lasted for.  It should be a reasonable fitness function, though you're free
        # to augment it with information from other stats as well
        fitness[n] = maxSize + turnsAlive / maxTurns

    return fitness

#
# def GaParentSelect(sorted_old_population, normalised_fitness):
#    parents = []
#    parent1 = np.random.choice(sorted_old_population, normalised_fitness)
#    parent2 = np.random.choice(sorted_old_population, normalised_fitness)
#
#    parents.append(parent1)
#    parents.append(parent2)
#
#    return parents


# Single-point crossover of 2 parent chromosomes.
# Random crossover point chosen
# with a 0.05 chance to mutate.
# Returns crossed over chromosome

def parentCrossover(parent1, parent2):
    crossoverPoint = random.randint(1, len(parent1[0])-1)
    crossedChromosome = np.concatenate((parent1[:, :crossoverPoint], parent2[:, crossoverPoint:]), axis=1)

    willMutate = random.uniform(0, 1)
    if willMutate < mutationChance:
        rowToMutate = random.randint(0, len(parent1)-1)
        colToMutate = random.randint(0, len(parent1[0])-1)
        newMutation = random.uniform(-10, 10)

        crossedChromosome[rowToMutate][colToMutate] = newMutation

    return crossedChromosome


# Training the new generation via stats gathered from param old_population
# Returns new generation of snakes.

def newGeneration(old_population):
    # This function should return a tuple consisting of:
    # - a list of the new_population of snakes that is of the same length as the old_population,
    # - the average fitness of the old population

    N = len(old_population)

    nPercepts = old_population[0].nPercepts
    actions = old_population[0].actions

    fitness = evalFitness(old_population)

    # At this point you should sort the old_population snakes according to fitness, setting it up for parent
    # selection.
    # .
    # .
    # .

    # sum the total population fitness and find the indexes
    # that sort the fitness list from lowest to highest

    total_fitness = np.sum(fitness)
    sort_index = np.argsort(fitness)

    # Sorting fitness array and population array based on above indexes

    sorted_fitness = np.array(fitness)[sort_index]
    sorted_old_population = np.array(old_population)[sort_index]
    normalised_fitness = np.zeros((N))

    # normalise fitness and place on interval from 0 to 1

    for n, x in enumerate(sorted_fitness):
        normalised_fitness[n] = x / total_fitness

    # Create new population list...
    new_population = list()
    for n in range(N):
        # Create a new snake
        new_snake = Snake(nPercepts, actions)

        # Here you should modify the new snakes chromosome by selecting two parents (based on their
        # fitness) and crossing their chromosome to overwrite new_snake.chromosome

        # Consider implementing elitism, mutation and various other
        # strategies for producing a new creature.

        # .
        # .
        # .

        # using np.random.choice to pick two parents based on their weights on the fitness interval
        # Roulette Wheel Selection - pseudocode found from
        # https://bit.ly/3dP0FnN

        parent1 = sorted_old_population[np.random.choice(len(sorted_old_population), replace=False, p=normalised_fitness)]
        parent2 = sorted_old_population[np.random.choice(len(sorted_old_population), replace=False, p=normalised_fitness)]
        # parent2 = np.random.choice(sorted_old_population, p=normalised_fitness)

        # Set new_snake chromosome 1, 2, and 3, to the crossed over parent chromosomes with a chance of mutation
        # for each new chromosome
        new_snake.chromosome1 = parentCrossover(parent1.chromosome1, parent2.chromosome1)
        new_snake.chromosome2 = parentCrossover(parent1.chromosome2, parent2.chromosome2)
        new_snake.chromosome3 = parentCrossover(parent1.chromosome3, parent2.chromosome3)

        # Add the new snake to the new population
        new_population.append(new_snake)

    # At the end you need to compute the average fitness and return it along with your new population
    avg_fitness = np.mean(fitness)

    return (new_population, avg_fitness)
