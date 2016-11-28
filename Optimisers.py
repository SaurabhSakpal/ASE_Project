from deap import base
from deap import creator
from deap import tools
from GAMethods import *
import random
from collections import defaultdict
import matplotlib.pyplot as plt

def nsga2Cdom(simulator, model):
    creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -1.0, 1.0, -1.0, 1.0), crowding_dist=None)
    creator.create("Individual", list, fitness=creator.FitnessMulti)
    toolbox = base.Toolbox()
    toolbox.register("splot_point", getIndividualPoint, simulator)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.splot_point)
    toolbox.register("evaluate", evaluateObjectives, model)
    toolbox.register("select", tools.selNSGA2Cdom)
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

    # printPopulation(pop)

    # print pop[0].fitness.valid
    # This is just to assign the crowding distance to the individuals
    # no actual selection is done
    #pop = toolbox.select(pop, MU)
    #print "\n After Selecting \n"
    #printPopulation(pop)
    NGEN = 10

    for gen in range(1, NGEN):
        # Vary the population
        #tools.assignCrowdingDist(pop)
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
        #record = stats.compile(pop)
        #logbook.record(gen=gen, evals=len(invalid_ind), **record)
        #print(logbook.stream)

    #print("Final population hypervolume is %f" % tools. hypervolume(pop, [11.0, 11.0]))

    # print "\n \n \nFinal Population: \n\n"
    # printPopulation(pop)

    return pop

def nsga2(simulator, model):
    creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -1.0, 1.0, -1.0, 1.0), crowding_dist=None)
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
    MU = 100
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

    # printPopulation(pop)

    # print pop[0].fitness.valid
    # This is just to assign the crowding distance to the individuals
    # no actual selection is done
    #pop = toolbox.select(pop, MU)
    #print "\n After Selecting \n"
    #printPopulation(pop)
    NGEN = 10

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

    # print "\n \n \nFinal Population: \n\n"
    # printPopulation(pop)

    return pop

def spea2(simulator, model):
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
    toolbox.register("mutate", mutatePoints, model)
    # binary tournament selection
    toolbox.register("selectTournament", tools.selTournament, tournsize=2)
    # ind1 = toolbox.individual()
    # print ind1
    # print ind1.fitness.valid
    MU = 12
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    # pop = toolbox.population(n=MU)
    # invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    # fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    # for ind, fit in zip(invalid_ind, fitnesses):
    #     ind.fitness.values = fit

    # Step 1 Initialization
    N = 80
    Nbar = 40
    GEN = 100
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
        if curr_gen >= GEN:
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

    printPopulation(pop)
    return pop


def ga(simulator, model):
    """ PSO implementation goes here """
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
    toolbox.register("mutate", mutatePoints, model)
    # binary tournament selection
    toolbox.register("selectTournament", tools.selTournament, tournsize=2)
    # ind1 = toolbox.individual()
    # print ind1
    # print ind1.fitness.valid
    MU = 24
    CXPB, MUTPB, NGEN = 0.5, 0.2, 10
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    pop = toolbox.population(n=MU)
    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    for g in range(NGEN):
        print("-- Generation %i --" % g)

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

        #print("  Evaluated %i individuals" % len(invalid_ind))

        # The population is entirely replaced by the offspring
        pop[:] = offspring

        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]

    #printPopulation(pop)
    return pop


def runOptimiser(simulator, model, algo):
   pop = algo(simulator, model)
   return [t.fitness.values for t in pop]
   #cost_nsga2 = [t.fitness.values[0] for t in pop_nsga2]
   #fr_nsga2 = [t.fitness.values[2] for t in pop_nsga2]
   #plt.show()
