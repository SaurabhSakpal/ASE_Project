from deap import base
from deap import creator
from deap import tools
from GAMethods import *
import random


def nsga2(simulator, model):
    creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -1.0, 1.0), crowding_dist=None)
    creator.create("Individual", list, fitness=creator.FitnessMulti)
    toolbox = base.Toolbox()
    toolbox.register("splot_point", getIndividualPoint, simulator)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.splot_point)
    toolbox.register("evaluate", evaluateObjectives, model)
    toolbox.register("select", tools.selNSGA2)
    toolbox.register("mate", matePoints, model)
    toolbox.register("mutate", mutatePoints, model)
    # ind1 = toolbox.individual()
    # print ind1
    # print ind1.fitness.valid
    MU = 12
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    pop = toolbox.population(n=MU)
    # print "\n\n\n ## \n"
    # print pop[0]
    # print toolbox.evaluate(pop[0])
    # print pop[0].fitness.valid

    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    printPopulation(pop)
    # print pop[0].fitness.valid
    # This is just to assign the crowding distance to the individuals
    # no actual selection is done
    #pop = toolbox.select(pop, MU)
    #print "\n After Selecting \n"
    #printPopulation(pop)
    NGEN = 12

    for gen in range(1, NGEN):
        # Vary the population
        #tools.assignCrowdingDist(pop)
        offspring = tools.selTournamentDCD(pop, len(pop))
        offspring = [toolbox.clone(ind) for ind in offspring]

        for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
            if random.random() <= 0.5:
                toolbox.mate(ind1, ind2)

            toolbox.mutate(ind1)
            toolbox.mutate(ind2)
            del ind1.fitness.values, ind2.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Select the next generation population
        pop = toolbox.select(pop + offspring, MU)
        #record = stats.compile(pop)
        #logbook.record(gen=gen, evals=len(invalid_ind), **record)
        #print(logbook.stream)

    #print("Final population hypervolume is %f" % tools. hypervolume(pop, [11.0, 11.0]))

    print "\n \n \nFinal Population: \n\n"
    printPopulation(pop)

    return pop


def spea2():
    """ SPEA2 implementation goes here """


def pso():
    """ PSO implementation goes here """


def runOptimiser(simulator, model):
    nsga2(simulator, model)
