import sys
import numpy as np
from parser import SPLOTParser
from Simulator import Simulator
from Optimisers import *
import GAMethods as ga

def main():
    assert len(sys.argv) == 2, "SPLOT Parser takes path to model.xml file as argument"
    modelFile = sys.argv[1]
    model = SPLOTParser().parse(modelFile)
    model.generateTreeStructureConstraints(model.root)

    simulator = Simulator(model)
    n = 1000
    costs = []
    violations = []
    num_features = []
    
    # print ga.getIndividualPoint(simulator)
    # exit()
    simulator.generateInitialPopulation()
    points = simulator.startPopulation
    non_violated_points = 0
    for point in points:
        #point.evaluateObjectives()
        cost, violation , num_feat = ga.evaluateObjectives(model,point)
        costs.append(cost)
        violations.append(violation)
        if violation ==0:
            non_violated_points += 1
        num_features.append(num_feat)

    print 'Mean cost', np.mean(costs)
    print 'Var cost', np.var(costs)
    print 'Mean violations', np.mean(violations)
    print 'Var violations', np.var(violations)
    print 'Mean num of features', np.mean(num_features)
    print 'Var num of features', np.var(num_features)
    plt.scatter(costs,num_features)
    plt.show()
    # plt.scatter(violations,num_features)
    # plt.show()

if __name__ == "__main__":
    main()