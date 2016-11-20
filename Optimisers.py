from deap import base
from deap import creator
from deap import tools
from GAMethods import *


def nsga2(simulator, model):
    creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -1.0, 1.0))
    creator.create("Individual", list, fitness=creator.FitnessMulti)
    toolbox = base.Toolbox()
    toolbox.register("splot_point", getIndividualPoint, simulator)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.splot_point)
    toolbox.register("evaluate", evaluateObjectives, model)
    toolbox.register("select", tools.selNSGA2)
    # ind1 = toolbox.individual()
    # print ind1
    # print ind1.fitness.valid
    MU = 10
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
    pop = toolbox.select(pop, 4)
    print "\n After Selecting \n"
    printPopulation(pop)


def spea2():
    """ SPEA2 implementation goes here """


def pso():
    """ PSO implementation goes here """


def runOptimiser(simulator, model):
    nsga2(simulator, model)
