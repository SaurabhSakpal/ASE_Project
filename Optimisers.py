from deap import base
from deap import creator
from deap import tools
from GAMethods import *
import random
from collections import defaultdict
import matplotlib.pyplot as plt

def nsga2Cdom(simulator, model, MU, NGEN, mutatePercentage):
    creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -1.0, 1.0, -1.0, 1.0), crowding_dist=None)
    creator.create("Individual", list, fitness=creator.FitnessMulti)
    toolbox = base.Toolbox()
    toolbox.register("splot_point", getIndividualPoint, simulator)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.splot_point)
    toolbox.register("evaluate", evaluateObjectives, model)
    toolbox.register("select", tools.selNSGA2Cdom)
    toolbox.register("mate", matePoints, model)

    toolbox.register("mutate", mutatePoints, model, mutatePercentage)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    pop = toolbox.population(n=MU)

    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    for gen in range(1, NGEN):
        offspring = tools.selTournamentDCDCdom(pop, len(pop))
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

    return pop

def nsga2(simulator, model, MU, NGEN, mutatePercentage):
    creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -1.0, 1.0, -1.0, 1.0), crowding_dist=None)
    creator.create("Individual", list, fitness=creator.FitnessMulti)
    toolbox = base.Toolbox()
    toolbox.register("splot_point", getIndividualPoint, simulator)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.splot_point)
    toolbox.register("evaluate", evaluateObjectives, model)
    toolbox.register("select", tools.selNSGA2)
    toolbox.register("mate", matePoints, model)
    toolbox.register("mutate", mutatePoints, model, mutatePercentage)

    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    pop = toolbox.population(n=MU)

    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    for gen in range(1, NGEN):
        # Vary the population
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

    return pop

def spea2(simulator, model, MU, NGEN, mutatePercentage):
    """ SPEA2 implementation goes here """
    simulator.setPopulationSize(100)
    simulator.generateInitialPopulation()
    creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -1.0, 1.0, -1.0, 1.0), crowding_dist=None)
    creator.create("Individual", list, fitness=creator.FitnessMulti)
    toolbox = base.Toolbox()
    toolbox.register("splot_point", getSATSolverGeneratedPoint, simulator)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.splot_point)
    toolbox.register("evaluate", evaluateObjectives, model)
    toolbox.register("select", tools.selSPEA2)
    toolbox.register("mate", matePoints, model)
    toolbox.register("mutate", mutatePoints, model, mutatePercentage)
    # binary tournament selection
    toolbox.register("selectTournament", tools.selTournament, tournsize=2)

    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # Step 1 Initialization
    N = 80
    Nbar = 40
    U = 0
    V = 1
    pop = toolbox.population(n=N)
    archive = []
    curr_gen = 1

    while True:
        # Step 2 Fitness assignement
        for ind in pop:
            ind.fitness.values = toolbox.evaluate(ind)

        for ind in archive:
            ind.fitness.values = toolbox.evaluate(ind)

        # Step 3 Environmental selection
        archive  = toolbox.select(pop + archive, k=Nbar)

        # Step 4 Termination
        if curr_gen >= NGEN:
            final_set = archive
            break

        # Step 5 Mating Selection
        mating_pool = toolbox.selectTournament(archive, k=N)
        offspring_pool = map(toolbox.clone, mating_pool)

        # Step 6 Variation
        # crossover 100% and mutation 6%
        for child1, child2 in zip(offspring_pool[::2], offspring_pool[1::2]):
            toolbox.mate(child1, child2)

        for mutant in offspring_pool:
            if random.random() < 0.06:
                toolbox.mutate(mutant)

        pop = offspring_pool

        curr_gen += 1

    return pop


def ga(simulator, model, MU, NGEN, mutatePercentage):
    """ GA implementation goes here """
    simulator.setPopulationSize(100)
    simulator.generateInitialPopulation()
    creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -1.0, 1.0, -1.0, 1.0), crowding_dist=None)
    creator.create("Individual", list, fitness=creator.FitnessMulti)
    toolbox = base.Toolbox()
    toolbox.register("splot_point", getSATSolverGeneratedPoint, simulator)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.splot_point)
    toolbox.register("evaluate", evaluateObjectives, model)
    toolbox.register("select", tools.selRandom)
    toolbox.register("mate", matePoints, model)
    toolbox.register("mutate", mutatePoints, model, mutatePercentage)
    toolbox.register("selectTournament", tools.selTournament, tournsize=2)

    CXPB, MUTPB = 0.5, 0.2
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    pop = toolbox.population(n=MU)
    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    for g in range(NGEN):
        #print("-- Generation %i --" % g)

        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):

            # cross two individuals with probability CXPB
            if random.random() < CXPB:
                toolbox.mate(child1, child2)

                # fitness values of the children
                # must be recalculated later
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:

            # mutate an individual with probability MUTPB
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # The population is entirely replaced by the offspring
        pop[:] = offspring

        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]

    return pop


def runOptimiser(simulator, model, optimiser, MU, NGEN, mutatePercentage):
   pop = optimiser(simulator, model, MU, NGEN, mutatePercentage)
   return [t.fitness.values for t in pop]
