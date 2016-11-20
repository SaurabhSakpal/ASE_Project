from deap import base
from deap import creator
from deap import tools

def getIndividualPoint(simulator):
    pointList = simulator.generateNPoints()
    #print "\n\n --------------------------------\n"
    #print pointList[0].value
    pointList[0].evaluateObjectives()
    #print pointList[0].objectives
    ind = [1 if i[1] == True else 0 for i in pointList[0].value]
    #print ind
    return ind

def evaluateObjectives(model, ind1):
    cost = evaluateCost(ind1, model)
    featureRichness = evaluateFeatureRichness(ind1)
    constraintsFailed = evaluateConstraintsFailed(ind1, model)
    return (cost, constraintsFailed,featureRichness)


def evaluateCost(ind1, model):
    """ Code for calculating cost of the given point goes here """
    # value = [[id1,True],[id2,True],[id3,False]...]
    # print 'find cost'
    return sum([model.treeNodeMap[model.nodeOrder[i]].cost if ind1[i] == 1 else 0 for i in range(len(ind1))])


def evaluateConstraintsFailed(ind1, model):
    """ Code for calculating how many constraints the point failed goes here """
    constraints_list = model.crossTreeConstraints
    leaves = [model.nodeOrder[i] for i in range(len(ind1)) if ind1[i] is 1]
    #leaves = [n[0] for n in self.value if n[1] is True]
    violations = 0
    for constraint in constraints_list:
        clauses = constraint.clauses
        isTrue = False
        for clause in clauses:
            node_id = clause[1:] if clause[0] == '~' else clause
            if (clause[0] == '~' and node_id not in leaves) or (clause[0] != '~' and node_id in leaves):
                isTrue = isTrue or True
        if not isTrue:
            violations += 1
    # print 'find violations'
    return violations


def evaluateFeatureRichness(ind1):
    """ Code for calculating Feature Richness of a point goes here """
    return sum(ind1)

def printPopulation(pop):
    for i in pop:
        print str(i) + " : " + str(i.fitness.values)



def runOptimiser(simulator, model):
    creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -1.0, 1.0))
    creator.create("Individual", list, fitness=creator.FitnessMulti)
    toolbox = base.Toolbox()
    toolbox.register("splot_point", getIndividualPoint, simulator)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.splot_point)
    toolbox.register("evaluate", evaluateObjectives, model)
    toolbox.register("select", tools.selNSGA2)
    #ind1 = toolbox.individual()
    #print ind1
    #print ind1.fitness.valid
    MU = 10
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    pop = toolbox.population(n=MU)
    #print "\n\n\n ## \n"
    #print pop[0]
    #print toolbox.evaluate(pop[0])
    #print pop[0].fitness.valid

    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    printPopulation(pop)
    #print pop[0].fitness.valid
    # This is just to assign the crowding distance to the individuals
    # no actual selection is done
    pop = toolbox.select(pop, 4)
    print "\n After Selecting \n"
    printPopulation(pop)