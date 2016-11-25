from __future__ import print_function
import sys
import numpy as np
from parser import SPLOTParser
from Simulator import Simulator
import numpy as np
from Optimisers import *
import matplotlib.pyplot as plt

def writeToFile(fitness, folder, pareto_name):
    fit_array = np.array(fitness, dtype=float)
    fit_array_norm = fit_array/ fit_array.max(axis=0)
    f = open(folder+pareto_name+'.txt','w')
    print(fit_array_norm.shape)
    for i in range(fit_array_norm.shape[0]):
        print(fit_array_norm[i,:])
        print(' '.join(map(str, fit_array_norm[i,:].tolist())), file=f)
    plt.scatter(fit_array_norm[:,0],fit_array_norm[:,2])
    plt.show()
    plt.scatter(fit_array[:,0],fit_array[:,2])
    plt.show()

def main():
    assert len(sys.argv) == 2, "SPLOT Parser takes path to model.xml file as argument"
    modelFile = sys.argv[1]
    model = SPLOTParser().parse(modelFile)
    model.generateTreeStructureConstraints(model.root)


    simulator = Simulator(model)
    n = 1000
    cost = []
    violations = []
    num_features = []
    folder_path = './Spread-HyperVolume/HyperVolume/Pareto_Fronts/'
    fitness_nsga2 = runOptimiser(simulator, model, nsga2)
    fitness_ga = runOptimiser(simulator, model, ga)
    writeToFile(fitness_nsga2, folder_path, modelFile.split('/')[1].split('.')[0]+'_nsga2')
    writeToFile(fitness_ga, folder_path, modelFile.split('/')[1].split('.')[0]+'_ga')

if __name__ == "__main__":
    main()