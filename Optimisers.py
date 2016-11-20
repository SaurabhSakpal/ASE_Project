from deap import base
from deap import creator
from deap import tools

def getIndividualPoint(simulator):
    pointList = simulator.generateNPoints()
    print "\n\n --------------------------------\n"
    print pointList[0].value
    pointList[0].evaluateObjectives()
    print pointList[0].objectives
    ind = [1 if i[1] == True else 0 for i in pointList[0].value]
    print ind
    return ind

def evaluatePoint(ind1):
    return (1,1,1)



def runOptimiser(simulator, model):
    creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -1.0, 1.0))
    creator.create("Individual", list, fitness=creator.FitnessMulti)
    toolbox = base.Toolbox()
    toolbox.register("splot_point", getIndividualPoint, simulator)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.splot_point)
    toolbox.register("evaluate", evaluatePoint)
    #ind1 = toolbox.individual()
    #print ind1
    #print ind1.fitness.valid
    MU = 1
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    pop = toolbox.population(n=MU)
    print "\n\n\n ## \n"
    print pop