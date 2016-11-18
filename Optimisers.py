from deap import base
from deap import creator
from deap import tools

def getIndividualPoint(pointList):
    return pointList[0]

def runOptimiser(pointList, simulator, model):
    creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -1.0, 1.0))
    creator.create("Individual", list, fitness=creator.FitnessMulti)
    toolbox = base.Toolbox()
    toolbox.register("splot_point", getIndividualPoint, pointList)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.splot_point, n=1)
    ind1 = toolbox.individual()
    print ind1
    print ind1.fitness.valid